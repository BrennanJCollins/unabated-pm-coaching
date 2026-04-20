#!/usr/bin/env python3
"""
Mentorship Transcript Evaluator
================================
Parses all structured mentorship transcripts (.md files with YAML frontmatter),
extracts Brennan's speaking turns, and produces a structured JSON evaluation
ready for LLM-based theme extraction and skill gap analysis.

Deterministic layer: file parsing, speaker extraction, metadata, word counts.
Probabilistic layer: theme tagging and quote selection (done by the LLM after).

Usage:
    python3 evaluate_transcripts.py --input-dir <transcripts_dir> --output <output.json>
    python3 evaluate_transcripts.py --input-dir <transcripts_dir> --output <output.json> --single <filename.md>
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path


def parse_yaml_frontmatter(text: str) -> dict:
    """Extract YAML frontmatter from markdown file."""
    match = re.match(r'^---\s*\n(.*?)\n---', text, re.DOTALL)
    if not match:
        return {}

    frontmatter = {}
    for line in match.group(1).strip().split('\n'):
        if ':' in line:
            key, _, value = line.partition(':')
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            frontmatter[key] = value
    return frontmatter


def extract_transcript_section(text: str) -> str:
    """Extract everything after ## Transcript heading."""
    match = re.search(r'^## Transcript\s*$', text, re.MULTILINE)
    if not match:
        return ""
    return text[match.end():]


def parse_speaker_turns(transcript_text: str) -> list[dict]:
    """Parse transcript into speaker turns.

    Handles two formats:
    1. **Speaker Name:** text (inline format, one per line)
    2. ### Speaker Name\\n\\ntext (heading format with body below)
    """
    turns = []

    # Try heading format first (### Speaker Name) — used in Office Hours / Fathom transcripts
    heading_pattern = re.compile(r'^###\s+(.+?)(?:\s*\(.*?\))?\s*$', re.MULTILINE)
    heading_matches = list(heading_pattern.finditer(transcript_text))

    if heading_matches:
        for i, match in enumerate(heading_matches):
            speaker = match.group(1).strip()
            start = match.end()
            end = heading_matches[i + 1].start() if i + 1 < len(heading_matches) else len(transcript_text)
            text = transcript_text[start:end].strip()
            if text:
                turns.append({"speaker": speaker, "text": text})
    else:
        # Bold format (**Speaker Name:** text) — used in ADPList transcripts
        # Note: colon is INSIDE the bold markers: **Name:** not **Name**:
        # Each turn is on its own line: **Name:** spoken text
        bold_pattern = re.compile(r'^\*\*(.+?):\*\*\s*(.+)$', re.MULTILINE)
        for match in bold_pattern.finditer(transcript_text):
            speaker = match.group(1).strip()
            text = match.group(2).strip()
            if text:
                turns.append({"speaker": speaker, "text": text})

    return turns


def extract_brennan_segments(turns: list[dict]) -> list[str]:
    """Extract and merge consecutive Brennan turns into coherent segments."""
    segments = []
    current_segment = []

    for turn in turns:
        is_brennan = "brennan" in turn["speaker"].lower()
        if is_brennan:
            current_segment.append(turn["text"])
        else:
            if current_segment:
                merged = " ".join(current_segment)
                # Only keep substantive segments (>50 chars, not just "Right." or "Mhmm.")
                if len(merged) > 50:
                    segments.append(merged)
                current_segment = []

    # Don't forget last segment
    if current_segment:
        merged = " ".join(current_segment)
        if len(merged) > 50:
            segments.append(merged)

    return segments


def extract_qa_pairs(turns: list[dict]) -> list[dict]:
    """Extract student question → Brennan answer pairs.

    A QA pair is: one or more consecutive non-Brennan turns (the question/context)
    followed by one or more consecutive Brennan turns (the answer).
    Only keeps pairs where both question and answer are substantive.
    """
    pairs = []
    current_question_parts = []
    current_answer_parts = []
    question_speaker = None
    in_answer = False

    for turn in turns:
        is_brennan = "brennan" in turn["speaker"].lower()

        if not is_brennan:
            # If we were building an answer, save the pair
            if in_answer and current_question_parts and current_answer_parts:
                q_text = " ".join(current_question_parts)
                a_text = " ".join(current_answer_parts)
                if len(q_text) > 30 and len(a_text) > 100:
                    pairs.append({
                        "student_context": q_text,
                        "brennan_response": a_text,
                        "student_speaker": question_speaker or "Student"
                    })

            # Start new question
            if not in_answer and current_question_parts:
                current_question_parts.append(turn["text"])
            else:
                current_question_parts = [turn["text"]]
                question_speaker = turn["speaker"]
            current_answer_parts = []
            in_answer = False
        else:
            in_answer = True
            current_answer_parts.append(turn["text"])

    # Final pair
    if current_question_parts and current_answer_parts:
        q_text = " ".join(current_question_parts)
        a_text = " ".join(current_answer_parts)
        if len(q_text) > 30 and len(a_text) > 100:
            pairs.append({
                "student_context": q_text,
                "brennan_response": a_text,
                "student_speaker": question_speaker or "Student"
            })

    return pairs


def extract_insights_and_highlights(text: str) -> dict:
    """Extract the Insights, Action Items, and Highlights sections."""
    sections = {}

    for section_name in ["Insights", "Action Items", "Highlights", "Key Takeaways", "Session Notes"]:
        pattern = rf'^## {section_name}\s*$(.*?)(?=^## |\Z)'
        match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
        if match:
            content = match.group(1).strip()
            if content and content != "---":
                sections[section_name.lower().replace(" ", "_")] = content

    return sections


def compute_stats(turns: list[dict], brennan_segments: list[str]) -> dict:
    """Compute basic stats about the transcript."""
    total_turns = len(turns)
    brennan_turns = sum(1 for t in turns if "brennan" in t["speaker"].lower())
    student_turns = total_turns - brennan_turns

    brennan_words = sum(len(t["text"].split()) for t in turns if "brennan" in t["speaker"].lower())
    student_words = sum(len(t["text"].split()) for t in turns if "brennan" not in t["speaker"].lower())

    return {
        "total_turns": total_turns,
        "brennan_turns": brennan_turns,
        "student_turns": student_turns,
        "brennan_word_count": brennan_words,
        "student_word_count": student_words,
        "substantive_brennan_segments": len(brennan_segments),
        "avg_segment_length_words": round(brennan_words / max(len(brennan_segments), 1)),
        "qa_density": round(brennan_words / max(student_words, 1), 2)
    }


def process_transcript(filepath: str) -> dict:
    """Process a single transcript file into structured evaluation data."""
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    metadata = parse_yaml_frontmatter(text)
    transcript_text = extract_transcript_section(text)
    pre_transcript = extract_insights_and_highlights(text)

    if not transcript_text:
        return {
            "file": os.path.basename(filepath),
            "metadata": metadata,
            "error": "No transcript section found",
            "pre_transcript_notes": pre_transcript
        }

    turns = parse_speaker_turns(transcript_text)
    brennan_segments = extract_brennan_segments(turns)
    qa_pairs = extract_qa_pairs(turns)
    stats = compute_stats(turns, brennan_segments)

    return {
        "file": os.path.basename(filepath),
        "metadata": metadata,
        "pre_transcript_notes": pre_transcript,
        "stats": stats,
        "brennan_segments": brennan_segments,
        "qa_pairs": qa_pairs
    }


def main():
    parser = argparse.ArgumentParser(description="Evaluate mentorship transcripts")
    parser.add_argument("--input-dir", required=True, help="Directory containing transcript .md files")
    parser.add_argument("--output", required=True, help="Output JSON file path")
    parser.add_argument("--single", help="Process only this specific file (filename, not full path)")
    parser.add_argument("--summary-only", action="store_true", help="Output metadata and stats only, skip full segments")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    if not input_dir.is_dir():
        print(f"Error: {input_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    # Collect files
    if args.single:
        files = [input_dir / args.single]
        if not files[0].exists():
            print(f"Error: {files[0]} does not exist", file=sys.stderr)
            sys.exit(1)
    else:
        files = sorted(input_dir.glob("*.md"))
        # Skip runbook and other non-transcript files
        files = [f for f in files if not f.name.startswith("_")]

    print(f"Processing {len(files)} transcript(s)...", file=sys.stderr)

    results = []
    for filepath in files:
        print(f"  → {filepath.name}", file=sys.stderr)
        result = process_transcript(str(filepath))

        if args.summary_only:
            # Strip large fields for summary view
            result.pop("brennan_segments", None)
            result.pop("qa_pairs", None)

        results.append(result)

    # Compute aggregate stats
    total_brennan_words = sum(r.get("stats", {}).get("brennan_word_count", 0) for r in results)
    total_segments = sum(r.get("stats", {}).get("substantive_brennan_segments", 0) for r in results)
    total_qa_pairs = sum(len(r.get("qa_pairs", [])) for r in results)

    output = {
        "aggregate": {
            "total_transcripts": len(results),
            "total_brennan_words": total_brennan_words,
            "total_substantive_segments": total_segments,
            "total_qa_pairs": total_qa_pairs,
            "avg_brennan_words_per_session": round(total_brennan_words / max(len(results), 1))
        },
        "transcripts": results
    }

    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\nDone. Output: {args.output}", file=sys.stderr)
    print(f"  Transcripts: {len(results)}", file=sys.stderr)
    print(f"  Total Brennan words: {total_brennan_words:,}", file=sys.stderr)
    print(f"  Substantive segments: {total_segments}", file=sys.stderr)
    print(f"  Q&A pairs: {total_qa_pairs}", file=sys.stderr)


if __name__ == "__main__":
    main()
