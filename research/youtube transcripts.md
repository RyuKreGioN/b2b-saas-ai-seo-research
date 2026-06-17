# B2B SaaS AI SEO Research

A structured research repository on **AI-powered SEO content production** — how modern practitioners build, automate, and scale content pipelines that rank in 2025–2026.

---

## Why This Topic

Search is in the middle of its biggest structural shift since 2012. AI Overviews, LLM-generated answers, and generative engine optimization (GEO) are rewriting what it means to "rank." At the same time, AI writing tools have commoditized low-effort content completely — meaning the old "publish more" playbook is dead.

This research maps what's actually working: the systems, workflows, tools, and mental models that practitioners are using to produce SEO content at scale *without* getting penalized or drowned out by AI-generated noise.

**Specific questions driving this research:**
- What does an AI-powered SEO content pipeline look like in 2026?
- How do top practitioners balance AI speed with E-E-A-T quality signals?
- What programmatic SEO patterns survive AI Overviews?
- How are B2B SaaS companies using AI to close the content gap vs. competitors?

---

## Expert Selection

10 practitioners were selected across the full content production stack. See [`/research/sources.md`](./research/sources.md) for full profiles, links, and annotations.

| Expert | Primary Focus | Channels |
|--------|--------------|---------|
| Nick Jordan | Content ops & programmatic SEO at scale | LinkedIn, Website |
| Kevin Indig | Organic growth strategy + AI Overview research | LinkedIn, Newsletter, Podcast |
| Eli Schwartz | Product-led SEO, AI disruption to content models | LinkedIn, Podcast, Book |
| Nathan Gotch | AI SEO frameworks, GEO | YouTube, Podcast |
| Aleyda Solís | Technical SEO + international + AI tooling | YouTube, LinkedIn, Newsletter |
| Ryan Law | Content quality in the AI era, thought leadership | LinkedIn, Newsletter |
| Kyle Roof | On-page AI optimization, scientific SEO testing | LinkedIn, YouTube, Tool |
| Glen Allsopp | Data-driven competitive content strategy | LinkedIn, Website |
| Matt Diggity | Performance SEO, AI content testing | YouTube, LinkedIn |
| Mordy Oberstein | SERP data analysis, AI Overviews tracking | LinkedIn, Podcast |

**Selection principle:** All 10 actively practice what they teach. They run agencies, build SEO tools, or manage in-house programs with documented results. Zero pure commentators.

---



## Content Collection Method

### LinkedIn Posts
LinkedIn does not provide a public API for post scraping. Posts are collected via one of these methods:
- **Manual:** Visit each expert's profile, copy their 5 most recent relevant posts into `/research/linkedin-posts/{author}/posts.md`
- **Phantom Buster / Apify:** LinkedIn Profile Scraper actor can automate this (requires a LinkedIn session cookie). See `/research/other/collection-notes.md` for setup instructions.
- **RapidAPI LinkedIn Scraper:** Available at `https://rapidapi.com/rockapis-rockapis-default/api/linkedin-data-api`

### YouTube Transcripts
Collected via the [Supadata YouTube Transcript API](https://supadata.ai/) or the free `youtube-transcript-api` Python library:

```bash
pip install youtube-transcript-api
python -c "
from youtube_transcript_api import YouTubeTranscriptApi
transcript = YouTubeTranscriptApi.get_transcript('VIDEO_ID')
print(' '.join([t['text'] for t in transcript]))
"
```

Or via Supadata API:
```bash
curl "https://api.supadata.ai/v1/youtube/transcript?videoId=VIDEO_ID" \
  -H "x-api-key: YOUR_KEY"
```

### Other Content
- Newsletters (Kevin Indig's Growth Memo, Ryan Law's Thinking Slow, Aleyda's SEOFOMO): Subscribe and save relevant issues to `/research/other/`
- Podcast episode summaries: Manually summarized from episode pages or RSS feeds

---

## Status

| Expert | LinkedIn Posts | YouTube Transcripts | Notes |
|--------|---------------|--------------------|----|
| Nick Jordan |  collected | N/A | No active YouTube channel |
| Kevin Indig |  collected | N/A | Podcast > YouTube |
| Eli Schwartz |  collected | N/A | Podcast appearances only |
| Nathan Gotch |  collected |  collected | Active YouTube |
| Aleyda Solís |  collected |  collected | Crawling Mondays |
| Ryan Law |  collected | N/A | Newsletter primary |
| Kyle Roof |  collected |  collected | Active YouTube |
| Glen Allsopp |  collected | N/A | Blog primary |
| Matt Diggity |  collected |  collected | Very active YouTube |
| Mordy Oberstein |  collected | N/A | Podcast + LinkedIn |

---

## Tools & Setup

### YouTube Transcript Scraping (Claude Code / local)

```bash
# Install dependencies
pip install youtube-transcript-api yt-dlp

# Get transcript for a single video
python scripts/get_transcript.py --video-id VIDEO_ID --author nathan-gotch

# Batch from a channel
python scripts/batch_transcripts.py --channel-url CHANNEL_URL --max 10
```

> Scripts are in `/scripts/` (to be added)
