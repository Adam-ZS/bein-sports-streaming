# BEIN Sports Streaming

|Free BEIN Sports streaming proxy — 12 channels with quality options, auto-updating matches table, and optimized HLS streaming. Works on mobile, TV, and desktop.

## Features

- **12 BEIN channels** — BEIN Sports 1-6 + BEIN Sports MAX 1-6
- **Quality options** — 360p / 480p / 720p / 1080p selector
- **Live matches table** — auto-updated via ESPN API, shows today's football schedule with BEIN channel mapping
- **Lag-optimized** — tuned HLS.js buffer (60s), smooth token refresh, auto-recovery on errors
- **Vercel deployment** — public URL, serverless Python functions
- **Mobile & TV friendly** — responsive dark theme, touch-optimized
- **Live/ended tags** — matches show 🔴LIVE or ✅انتهت badges
- **Click-to-watch** — tap any match card to switch to its BEIN channel

## Quick Start

Visit: https://adam-bein.vercel.app

### Local Proxy (for lower latency)

```bash
python3 bein-server-v6.py
# → http://localhost:8000
```

## API Endpoints

| Endpoint | Description |
|---|---|
| `/` | Main streaming UI (12 channels + matches + quality selector) |
| `/api/channel?ch=CHANNEL&q=QUALITY` | Get stream token (q=360/480/720/1080) |
| `/api/proxy?url=URL` | Proxy M3U8/TS segments with BuzCup UA |
| `/api/matches` | Live football schedule with BEIN channel mapping |

### Sources

| Source | Description | Qualities |
|---|---|---|
| **man1ted** (رئيسي) | Primary source via API with BuzCup UA | 360p / 480p / 720p / 1080p |
| **VACO** (احتياطي) | Cloudflare R2 direct M3U8 (no proxy needed) | Single quality |
| **YallaHD** (إضافي) | Cloudflare Workers hosted Arabic BEIN | Single quality |
| **Amagi** (مجاني) | US BEIN XTRA free ad-supported | 720p / 1080p |

### Channel IDs

- `beee1-6` — BEIN Sports 1-6
- `beemax1-6` — BEIN MAX 1-6

## What's New (v2)

- **Quality selector** — different &q= parameter values for source quality negotiation
- **Dynamic matches** — table fetches from ESPN API on load, auto-refreshes every 10min
- **Smooth playback** — HLS.js tuned with 60s buffer, disabled lowLatencyMode (causes stutter), auto-reconnect on errors
- **Token refresh** — pre-loads new stream URL before 600s expiry, no interruption
- **Cold start warm-up** — pre-pings API on page load to reduce first-play latency
