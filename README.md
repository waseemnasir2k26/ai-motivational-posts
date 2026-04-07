# AI Motivational Posts — Built in Minutes With Claude Code

> Generate Tommy Mello tweet-style motivational quote cards + a ready-to-import GoHighLevel scheduling CSV from a single JSON file. **Zero design tools. Zero Canva. Zero clicks.**

![Sample quote card](output/images/quote_01.png)

This entire repo — Python image generator, GHL CSV builder, PDF guide, scheduling logic — was built in **one conversation with [Claude Code](https://www.anthropic.com/claude-code)**. Fork it, swap your photo, edit one JSON file, run two scripts, and you have 10 perfectly-branded motivational posts scheduled across every social platform.

---

## What's inside

```
ai-motivational-posts/
├── posts.json              ← edit this. The single source of truth.
├── photo.png               ← swap with your own headshot
├── generate_images.py      ← renders 1080x1350 PNG quote cards (PIL)
├── build_csv.py            ← builds GHL Advanced 39-col bulk CSV
├── preview.html            ← visual preview of all 10 cards in browser
├── output/
│   ├── images/             ← 10 generated PNGs
│   └── ghl-batch4-quotes.csv  ← ready-to-import GHL CSV
└── docs/
    └── HOW-TO-GUIDE.pdf    ← shareable PDF walkthrough
```

---

## Quick start (60 seconds)

```bash
# 1. Clone
git clone https://github.com/waseemnasir2k26/ai-motivational-posts.git
cd ai-motivational-posts

# 2. Install one dependency
pip install Pillow

# 3. Replace photo.png with your headshot (square works best)

# 4. Edit posts.json — change author name/handle and the 10 quotes

# 5. Generate images
python generate_images.py

# 6. Generate the GHL CSV
python build_csv.py
```

That's it. Output lands in `output/`. Upload the CSV to GoHighLevel via:
**Marketing → Social Planner → Bulk Upload → Advanced**.

---

## Why this exists

Most "motivational quote" creators are clunky: Canva templates that take 20 minutes per post, AI image generators that hallucinate text, or scheduling tools that don't talk to your CRM. This repo collapses the entire pipeline into **one JSON file + two Python scripts**.

- **Data-driven** — every quote, caption, hashtag, and schedule slot lives in `posts.json`
- **Brand-consistent** — same avatar, same layout, same colors across every card
- **Schedule-aware** — auto-assigns USA-optimized posting times by weekday
- **Multi-platform** — the GHL CSV pushes to Facebook, Instagram, LinkedIn, YouTube Shorts, TikTok, Pinterest, GBP, and Community in one upload
- **Forkable** — open-source MIT, no vendor lock-in

---

## How it was built (the Claude Code workflow)

This is the actual conversation flow that produced this repo:

1. **"Show me 10 motivational AI quotes in a Tommy Mello tweet style with my photo"**
   → Claude wrote `preview.html` with 10 quote cards, captions, and hashtags I could approve in the browser.

2. **"These look great. Now turn them into PNGs."**
   → Claude wrote `generate_images.py` using Pillow. Reads `posts.json`, outputs 1080x1350 cards.

3. **"Now build the GoHighLevel Advanced bulk-CSV with these 10 posts scheduled across two weeks."**
   → Claude wrote `build_csv.py` matching GHL's exact 39-column format with platform-specific fields.

4. **"Make this a public GitHub repo so anyone can copy it."**
   → Claude refactored everything into a clean folder structure, wrote this README, and generated a PDF guide.

**Total time: one conversation.** No Photoshop, no Canva, no manual CSV editing.

---

## Customizing for your brand

### Change quotes
Open `posts.json` and edit the `posts` array. Each post needs:
- `quote` — the text shown on the card (use `\n` for line breaks)
- `caption` — the long-form caption used in the social post
- `hashtags` — space-separated hashtags

### Change author identity
Edit the `author` block at the top of `posts.json`:
```json
"author": {
  "name": "Your Name",
  "handle": "@yourhandle",
  "photo": "photo.png"
}
```
Then drop your headshot in as `photo.png` (square crop, ~500x500 minimum).

### Change schedule
The `schedule.times_by_weekday` block lets you set a different posting time per day of the week. Change `start_date` to whenever you want the first post to go live.

### Change image hosting
Open `build_csv.py` and edit `REPO_RAW_URL` to point at your fork's `raw.githubusercontent.com` URL. GHL needs publicly-reachable image URLs — GitHub raw URLs work, Google Drive does not.

---

## The exact prompts to give Claude Code

Want to recreate this from scratch (or build a variant)? Paste these into Claude Code in order:

```
1. "Create 10 motivational quote ideas for [your niche] in a Tommy Mello tweet
    style. Each one needs: a 1-2 sentence quote, a 4-line caption,
    and 10 mixed-tier hashtags. Show them in an HTML preview
    with my headshot."

2. "I approve these. Write a Python script using Pillow that reads a JSON
    file and renders each quote as a 1080x1350 PNG: white card, black
    top/bottom bars, circular avatar with green glow, blue verified
    badge next to my name, bold quote text auto-shrunk to fit."

3. "Now write a Python script that reads the same JSON and outputs a
    GoHighLevel Advanced bulk-post CSV (39 columns, 2-row header).
    Schedule one post per day starting [date], using these times by
    weekday: Mon 9am, Tue 12pm, Wed 10am, Thu 2pm, Fri 5pm,
    Sat 11am, Sun 10am EST."

4. "Refactor the whole thing into a clean repo, write a README that
    tells the story of how Claude Code built it, and generate a
    shareable PDF guide."
```

---

## Tech

- **Python 3.11+**
- **Pillow** (PIL) for image generation
- **csv** (stdlib) for the GHL CSV
- **ReportLab** (PDF guide only)

No external APIs. No paid services. Runs offline.

---

## License

MIT. Fork it, ship it, sell it, remix it. Credit appreciated but not required.

---

## Built by

**[Waseem Nasir](https://www.waseemnasir.com)** — founder of [SkynetJoe / Skynet Labs](https://www.skynetjoe.com).
I build AI agents, automation systems, and revenue machines for agencies and startups.

- Twitter / X: [@waseemnasir](https://twitter.com/waseemnasir)
- GitHub: [github.com/waseemnasir2k26](https://github.com/waseemnasir2k26)
- 47 free tools: [skynetlabs-toolkit.vercel.app](https://skynetlabs-toolkit.vercel.app)

If this saved you time, share the repo and tag me. Let's flood the timeline with content built in minutes, not hours.
