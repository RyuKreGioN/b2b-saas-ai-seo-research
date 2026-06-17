# Content Collection Notes & Setup Guide

## Overview

This document covers the technical setup for collecting content from each channel type.

---

## 1. YouTube Transcripts

### Method A: youtube-transcript-api (free, no key needed)

```bash
pip install youtube-transcript-api
```

```python
from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript(video_id: str) -> str:
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return " ".join([t["text"] for t in transcript])

# Example — Nathan Gotch video
print(get_transcript("VIDEO_ID_HERE"))
```

**Limitations:** Only works if the video has captions (auto or manual). Fails on some videos with disabled transcripts.

### Method B: Supadata API (more reliable, requires free API key)

Sign up at https://supadata.ai/ — free tier available.

```bash
curl "https://api.supadata.ai/v1/youtube/transcript?videoId=VIDEO_ID" \
  -H "x-api-key: YOUR_SUPADATA_KEY"
```

### Method C: yt-dlp (local, extracts auto-captions)

```bash
pip install yt-dlp

# Download auto-generated subtitles as SRT
yt-dlp --write-auto-sub --skip-download --sub-format srt -o "%(id)s.%(ext)s" "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Target Videos Per Expert

| Expert | Channel URL | Target Videos |
|--------|------------|--------------|
| Nathan Gotch | https://www.youtube.com/@NathanGotch | 3 most recent AI SEO videos |
| Aleyda Solís | https://www.youtube.com/@AleydaSolis | 3 most recent Crawling Mondays |
| Kyle Roof | https://www.youtube.com/@KyleRoofSEO | 3 most recent AI/content videos |
| Matt Diggity | https://www.youtube.com/@MattDiggity | 3 most recent AI content videos |

---

## 2. LinkedIn Posts

LinkedIn has no official public API for post scraping.

### Method A: Manual (recommended for small batches)

1. Go to each expert's LinkedIn profile
2. Click **"Posts"** in the activity filter
3. Copy-paste each relevant post into the corresponding `/research/linkedin-posts/{author}/posts.md`
4. Note: date, engagement count, and add a 1-sentence annotation

### Method B: Apify LinkedIn Scraper (automated)

URL: https://apify.com/curious_coder/linkedin-post-search-scraper

- Requires: LinkedIn session cookies (from your own account)
- Cost: ~$5–10 for a batch run
- Output: JSON → convert to Markdown

### Method C: PhantomBuster LinkedIn Profile Scraper

URL: https://phantombuster.com/automations/linkedin/2818/linkedin-profile-scraper

- More feature-rich but requires LinkedIn session cookies
- Free trial available

### Method D: RapidAPI

URL: https://rapidapi.com/rockapis-rockapis-default/api/linkedin-data-api

```bash
curl --request GET \
  --url 'https://linkedin-data-api.p.rapidapi.com/get-profile-posts?username=nickfromseattle&start=0' \
  --header 'X-RapidAPI-Key: YOUR_KEY' \
  --header 'X-RapidAPI-Host: linkedin-data-api.p.rapidapi.com'
```

---

## 3. Newsletters

Subscribe to each newsletter and save relevant recent issues:

| Newsletter | URL | Frequency |
|-----------|-----|-----------|
| The Growth Memo (Kevin Indig) | https://www.kevin-indig.com/ | Weekly |
| Thinking Slow (Ryan Law) | https://www.thinkingslow.com/ | Weekly |
| SEOFOMO (Aleyda Solís) | https://www.seofomo.co/ | Weekly |

Save as: `/research/other/newsletters/{author}/{date}-{slug}.md`

---

## 4. Podcast Episodes

For podcast transcripts, use:

### Podscribe / Podtext

- https://podtext.ai/ — paste a podcast episode URL, get a transcript
- Works with most major podcast RSS feeds

### Manual from show notes

Some episodes (especially Kevin Indig's Contrarian Marketing) publish edited transcripts on their website.

Target episodes for each podcast:

| Podcast | Host | Target |
|---------|------|--------|
| The AI Search Report | Nathan Gotch | Last 3 episodes |
| Contrarian Marketing | Kevin Indig + Eli Schwartz | Last 3 episodes |
| SERP's Up | Mordy Oberstein | Last 2 episodes |
| Crawling Mondays | Aleyda Solís | Last 2 episodes |

---

## File Naming Convention

```
/research/linkedin-posts/{author-slug}/posts.md          # All posts in one file
/research/youtube-transcripts/{author-slug}/{video-id}_{title-slug}.md
/research/other/newsletters/{author-slug}/{YYYY-MM-DD}_{title-slug}.md
/research/other/podcasts/{author-slug}/{YYYY-MM-DD}_{title-slug}.md
```

---

## Claude Code / Automation Script (suggested)

Once you have Supadata + RapidAPI keys, you can automate the full pipeline:

```bash
# Install deps
pip install youtube-transcript-api requests

# Run batch collection
python scripts/collect_all.py \
  --supadata-key YOUR_KEY \
  --rapidapi-key YOUR_KEY \
  --experts all
```

> `scripts/collect_all.py` — to be built from the individual fetch utilities above.
