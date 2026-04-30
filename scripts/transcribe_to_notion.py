#!/usr/bin/env python3
"""Watch a directory for new audio files, transcribe with Whisper, post a summary to Notion.

Flow
----
1. A new audio file lands in AUDIO_DIR.
2. Whisper (running locally) transcribes it.
3. A short summary is generated (heuristic, or via OpenAI when OPENAI_API_KEY is set).
4. A page is created in the configured Notion database with the summary and full transcript.

Human checkpoint
----------------
On the very first transcription the script writes the transcript next to the audio file
and waits for the user to confirm before posting to Notion. A marker file
(``.first_verified``) is written under AUDIO_DIR; subsequent files post automatically.

Required environment variables
------------------------------
NOTION_API_KEY        Notion integration token (https://www.notion.so/my-integrations)
NOTION_DATABASE_ID    Target database id (the integration must be shared with it)

Optional environment variables
------------------------------
AUDIO_DIR             Directory to watch (default: ./recordings)
WHISPER_MODEL         Whisper model size: tiny|base|small|medium|large (default: base)
OPENAI_API_KEY        If set, used to produce a higher-quality 3-5 sentence summary

Usage
-----
    python scripts/transcribe_to_notion.py                # watch AUDIO_DIR
    python scripts/transcribe_to_notion.py path/to/x.wav  # one-shot

Dependencies
------------
    pip install openai-whisper notion-client watchdog python-dotenv
    # Whisper also needs ffmpeg available on PATH.
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".mp4", ".webm", ".ogg", ".flac"}
NOTION_TEXT_LIMIT = 2000  # Notion rich_text blocks cap at 2000 chars
FIRST_VERIFIED_MARKER = ".first_verified"
PROCESSED_MARKER = ".processed"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("transcribe_to_notion")


def load_whisper(model_name: str):
    import whisper  # imported lazily so the script can `--help` without the dep
    log.info("Loading Whisper model %r (first load downloads weights)…", model_name)
    return whisper.load_model(model_name)


def transcribe(model, audio_path: Path) -> str:
    log.info("Transcribing %s", audio_path.name)
    result = model.transcribe(str(audio_path))
    return result["text"].strip()


def summarize(transcript: str) -> str:
    """Return a short summary. Uses OpenAI if OPENAI_API_KEY is set, else a heuristic."""
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Summarize call transcripts in 3-5 sentences. "
                                                  "Capture purpose, key decisions, and follow-ups."},
                    {"role": "user", "content": transcript[:12000]},
                ],
                temperature=0.2,
            )
            return resp.choices[0].message.content.strip()
        except Exception as exc:
            log.warning("OpenAI summary failed (%s); falling back to heuristic.", exc)

    sentences = transcript.replace("\n", " ").split(". ")
    head = ". ".join(sentences[:4]).strip()
    if head and not head.endswith("."):
        head += "."
    return head or transcript[:500]


def chunk_text(text: str, size: int = NOTION_TEXT_LIMIT) -> list[str]:
    return [text[i:i + size] for i in range(0, len(text), size)] or [""]


def post_to_notion(database_id: str, audio_path: Path, summary: str, transcript: str) -> str:
    from notion_client import Client

    notion = Client(auth=os.environ["NOTION_API_KEY"])
    title = f"Call: {audio_path.stem}"

    children = [
        {"object": "block", "type": "heading_2",
         "heading_2": {"rich_text": [{"type": "text", "text": {"content": "Summary"}}]}},
        *[{"object": "block", "type": "paragraph",
           "paragraph": {"rich_text": [{"type": "text", "text": {"content": chunk}}]}}
          for chunk in chunk_text(summary)],
        {"object": "block", "type": "heading_2",
         "heading_2": {"rich_text": [{"type": "text", "text": {"content": "Transcript"}}]}},
        *[{"object": "block", "type": "paragraph",
           "paragraph": {"rich_text": [{"type": "text", "text": {"content": chunk}}]}}
          for chunk in chunk_text(transcript)],
    ]

    page = notion.pages.create(
        parent={"database_id": database_id},
        properties={
            "Name": {"title": [{"text": {"content": title}}]},
        },
        children=children,
    )
    return page["url"]


def human_checkpoint(audio_dir: Path, audio_path: Path, transcript: str, summary: str) -> bool:
    """Pause for human verification before the very first Notion post."""
    marker = audio_dir / FIRST_VERIFIED_MARKER
    if marker.exists():
        return True

    transcript_path = audio_path.with_suffix(audio_path.suffix + ".transcript.txt")
    transcript_path.write_text(
        f"# Transcript for {audio_path.name}\n# Generated: {datetime.now().isoformat()}\n\n"
        f"## Summary\n{summary}\n\n## Transcript\n{transcript}\n",
        encoding="utf-8",
    )

    log.info("=" * 60)
    log.info("HUMAN CHECKPOINT — review the first transcription before posting.")
    log.info("Transcript written to: %s", transcript_path)
    log.info("=" * 60)
    answer = input("Post to Notion and continue automatically from here on? [y/N]: ").strip().lower()
    if answer != "y":
        log.info("Aborted by user. Re-run after editing %s if needed.", transcript_path)
        return False

    marker.write_text(f"verified={datetime.now().isoformat()}\nfile={audio_path.name}\n")
    return True


def already_processed(audio_path: Path) -> bool:
    return (audio_path.with_suffix(audio_path.suffix + PROCESSED_MARKER)).exists()


def mark_processed(audio_path: Path, notion_url: str) -> None:
    (audio_path.with_suffix(audio_path.suffix + PROCESSED_MARKER)).write_text(
        f"processed_at={datetime.now().isoformat()}\nnotion_url={notion_url}\n"
    )


def process_file(model, audio_path: Path, audio_dir: Path, database_id: str) -> Optional[str]:
    if already_processed(audio_path):
        log.info("Skipping %s (already processed).", audio_path.name)
        return None

    transcript = transcribe(model, audio_path)
    if not transcript:
        log.warning("Empty transcript for %s; skipping.", audio_path.name)
        return None

    summary = summarize(transcript)

    if not human_checkpoint(audio_dir, audio_path, transcript, summary):
        return None

    url = post_to_notion(database_id, audio_path, summary, transcript)
    mark_processed(audio_path, url)
    log.info("Posted to Notion: %s", url)
    return url


def watch_directory(model, audio_dir: Path, database_id: str) -> None:
    from watchdog.events import FileSystemEventHandler
    from watchdog.observers import Observer

    class Handler(FileSystemEventHandler):
        def on_created(self, event):
            if event.is_directory:
                return
            path = Path(event.src_path)
            if path.suffix.lower() not in AUDIO_EXTENSIONS:
                return
            # wait briefly for the file to finish being written
            time.sleep(2)
            try:
                process_file(model, path, audio_dir, database_id)
            except Exception:
                log.exception("Failed to process %s", path)

    log.info("Watching %s for new audio files. Ctrl-C to stop.", audio_dir)
    # process anything already sitting in the directory
    for existing in sorted(audio_dir.iterdir()):
        if existing.is_file() and existing.suffix.lower() in AUDIO_EXTENSIONS:
            try:
                process_file(model, existing, audio_dir, database_id)
            except Exception:
                log.exception("Failed to process %s", existing)

    observer = Observer()
    observer.schedule(Handler(), str(audio_dir), recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("file", nargs="?", help="Single audio file to process (otherwise watch AUDIO_DIR).")
    parser.add_argument("--audio-dir", default=os.getenv("AUDIO_DIR", "./recordings"))
    parser.add_argument("--model", default=os.getenv("WHISPER_MODEL", "base"))
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    for var in ("NOTION_API_KEY", "NOTION_DATABASE_ID"):
        if not os.getenv(var):
            log.error("Missing required environment variable: %s", var)
            return 2
    database_id = os.environ["NOTION_DATABASE_ID"]

    audio_dir = Path(args.audio_dir).expanduser().resolve()
    audio_dir.mkdir(parents=True, exist_ok=True)

    model = load_whisper(args.model)

    if args.file:
        path = Path(args.file).expanduser().resolve()
        if not path.exists():
            log.error("File not found: %s", path)
            return 1
        process_file(model, path, audio_dir, database_id)
        return 0

    watch_directory(model, audio_dir, database_id)
    return 0


if __name__ == "__main__":
    sys.exit(main())
