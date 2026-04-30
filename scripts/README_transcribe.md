# Audio → Notion transcription pipeline

`transcribe_to_notion.py` watches a directory for new recorded calls, transcribes
them locally with OpenAI's Whisper, and posts a summary + full transcript to a
Notion database.

## Setup

```bash
pip install -r scripts/requirements-transcribe.txt
# Whisper requires ffmpeg on PATH:
#   macOS:   brew install ffmpeg
#   Ubuntu:  sudo apt install ffmpeg
```

Copy `.env.example` to `.env` and fill in:

- `NOTION_API_KEY` — internal integration token
- `NOTION_DATABASE_ID` — target database (share it with the integration)
- `AUDIO_DIR` — directory the watcher monitors (default `./recordings`)
- `WHISPER_MODEL` — `tiny|base|small|medium|large` (default `base`)
- `OPENAI_API_KEY` *(optional)* — switches summaries from heuristic to LLM

The Notion database must have a `Name` (title) property.

## Usage

```bash
# Watch mode (default): drop audio files into AUDIO_DIR and they get processed
python scripts/transcribe_to_notion.py

# One-shot: process a single file
python scripts/transcribe_to_notion.py path/to/call.mp3
```

## Human checkpoint

The first transcription pauses for review. The script writes
`<audio>.transcript.txt` next to the audio file and prompts you to confirm before
posting to Notion. After confirmation a `.first_verified` marker is written to
`AUDIO_DIR` and subsequent files post automatically.

Each processed file gets a `<audio>.processed` sibling file recording the Notion
page URL — delete it to re-process the same audio.
