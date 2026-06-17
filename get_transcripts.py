#!/usr/bin/env python3
"""
Batch YouTube transcript collector for b2b-saas-ai-seo-research.
Uses youtube-transcript-api (free, no key needed) with Supadata as fallback.

Usage:
    python scripts/get_transcripts.py --video-id VIDEO_ID --author nathan-gotch
    python scripts/get_transcripts.py --channel https://www.youtube.com/@NathanGotch --max 5 --author nathan-gotch
"""

import argparse
import os
import re
import json
from datetime import datetime

try:
    from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
    YTAPI_AVAILABLE = True
except ImportError:
    YTAPI_AVAILABLE = False
    print("WARNING: youtube-transcript-api not installed. Run: pip install youtube-transcript-api")

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("WARNING: requests not installed. Run: pip install requests")


EXPERTS = {
    "nathan-gotch": {
        "channel": "https://www.youtube.com/@NathanGotch",
        "channel_id": "UCKaE1MiRPCTFXLFhH5VGiMQ",  # update if wrong
    },
    "aleyda-solis": {
        "channel": "https://www.youtube.com/@AleydaSolis",
        "channel_id": "UCKaE1MiRPCTFXLFhH5VGiMQ",  # placeholder — update
    },
    "kyle-roof": {
        "channel": "https://www.youtube.com/@KyleRoofSEO",
        "channel_id": "",  # placeholder — update
    },
    "matt-diggity": {
        "channel": "https://www.youtube.com/@MattDiggity",
        "channel_id": "",  # placeholder — update
    },
}


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text[:60]


def get_transcript_ytapi(video_id: str) -> str | None:
    """Fetch transcript using youtube-transcript-api."""
    if not YTAPI_AVAILABLE:
        return None
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([t["text"] for t in transcript])
    except (TranscriptsDisabled, NoTranscriptFound):
        print(f"  No transcript available for {video_id}")
        return None
    except Exception as e:
        print(f"  Error fetching transcript for {video_id}: {e}")
        return None


def get_transcript_supadata(video_id: str, api_key: str) -> str | None:
    """Fallback: Fetch transcript via Supadata API."""
    if not REQUESTS_AVAILABLE or not api_key:
        return None
    try:
        resp = requests.get(
            f"https://api.supadata.ai/v1/youtube/transcript",
            params={"videoId": video_id},
            headers={"x-api-key": api_key},
            timeout=30,
        )
        if resp.status_code == 200:
            data = resp.json()
            segments = data.get("content", [])
            return " ".join([s.get("text", "") for s in segments])
        else:
            print(f"  Supadata error {resp.status_code}: {resp.text[:200]}")
            return None
    except Exception as e:
        print(f"  Supadata request failed: {e}")
        return None


def save_transcript(author: str, video_id: str, title: str, transcript: str, output_dir: str):
    """Save transcript to the correct folder."""
    folder = os.path.join(output_dir, "research", "youtube-transcripts", author)
    os.makedirs(folder, exist_ok=True)

    filename = f"{video_id}_{slugify(title)}.md"
    filepath = os.path.join(folder, filename)

    content = f"""# {title}
**Video ID:** {video_id}
**URL:** https://www.youtube.com/watch?v={video_id}
**Author:** {author}
**Collected:** {datetime.now().strftime('%Y-%m-%d')}

## Transcript

{transcript}

---

## Key Takeaways

- [ ] Add takeaway 1 (relevant to AI SEO content production)
- [ ] Add takeaway 2
- [ ] Add takeaway 3
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"  Saved: {filepath}")
    return filepath


def process_video(video_id: str, author: str, title: str = "Unknown Title",
                  output_dir: str = ".", supadata_key: str = ""):
    """Fetch and save transcript for a single video."""
    print(f"\nProcessing: {video_id} ({author})")

    transcript = get_transcript_ytapi(video_id)

    if not transcript and supadata_key:
        print("  Falling back to Supadata...")
        transcript = get_transcript_supadata(video_id, supadata_key)

    if transcript:
        save_transcript(author, video_id, title, transcript, output_dir)
        return True
    else:
        print(f"  FAILED: Could not retrieve transcript for {video_id}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Batch YouTube transcript collector")
    parser.add_argument("--video-id", help="Single YouTube video ID")
    parser.add_argument("--title", default="Unknown Title", help="Video title (for single video mode)")
    parser.add_argument("--author", required=True, help="Expert slug (e.g. nathan-gotch)")
    parser.add_argument("--supadata-key", default="", help="Supadata API key (optional fallback)")
    parser.add_argument("--output-dir", default=".", help="Root of the research repo")
    args = parser.parse_args()

    if args.video_id:
        process_video(
            video_id=args.video_id,
            author=args.author,
            title=args.title,
            output_dir=args.output_dir,
            supadata_key=args.supadata_key,
        )
    else:
        print("Please provide --video-id. Channel scraping requires YouTube Data API v3.")
        print("Example:")
        print("  python scripts/get_transcripts.py --video-id dQw4w9WgXcQ --author nathan-gotch --title 'My Video Title'")


if __name__ == "__main__":
    main()
