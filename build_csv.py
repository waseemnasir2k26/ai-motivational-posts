"""
build_csv.py
------------
Reads posts.json and outputs a GoHighLevel (GHL) Advanced bulk-post CSV
(39 columns with a 2-row header) ready to import via:
  Marketing > Social Planner > Bulk Upload > Advanced.

Schedules 10 posts starting at `schedule.start_date` using the
times_by_weekday table. Image URLs point to the raw GitHub content URL of
this repository — edit `REPO_RAW_URL` before running if you fork the repo.

Usage:
    python build_csv.py

Output:
    output/ghl-batch4-quotes.csv
"""

import csv
import json
from datetime import datetime, timedelta
from pathlib import Path

# ---------- CONFIG ----------
ROOT = Path(__file__).parent
POSTS_FILE = ROOT / "posts.json"
OUT_CSV = ROOT / "output" / "ghl-batch4-quotes.csv"

# Edit this to match your fork. Images must be publicly accessible.
REPO_RAW_URL = (
    "https://raw.githubusercontent.com/"
    "waseemnasir2k26/ai-motivational-posts/main/output/images"
)

# Advanced-CSV 2-row header (matches the official GHL template exactly)
HEADER_ROW_1 = [
    "All Social", "All Social", "All Social", "All Social", "All Social",
    "All Social", "All Social", "All Social", "All Social", "All Social",
    "All Social",
    "Facebook",
    "Instagram",
    "LinkedIn", "LinkedIn",
    "Google (GBP)", "Google (GBP)", "Google (GBP)", "Google (GBP)",
    "Google (GBP)", "Google (GBP)", "Google (GBP)", "Google (GBP)",
    "Google (GBP)", "Google (GBP)",
    "YouTube", "YouTube", "YouTube",
    "TikTok", "TikTok", "TikTok", "TikTok", "TikTok", "TikTok", "TikTok",
    "Community", "Community",
    "Pinterest", "Pinterest",
]

HEADER_ROW_2 = [
    "postAtSpecificTime (YYYY-MM-DD HH:mm:ss)",
    "content",
    "OGmetaUrl (url)",
    "imageUrls (comma-separated)",
    "gifUrl",
    "videoUrls (comma-separated)",
    "mediaOptimization (true/false)",
    "applyWatermark (true/false)",
    "tags (comma-separated)",
    "category",
    "followUpComment",
    "type (post/story/reel)",
    "type (post/story/reel)",
    "pdfTitle",
    "postAsPdf (true/false)",
    "eventType (call_to_action/event/offer)",
    "actionType (none/order/book/shop/learn_more/call/sign_up)",
    "title",
    "offerTitle",
    "startDate (YYYY-MM-DD HH:mm:ss)",
    "endDate (YYYY-MM-DD HH:mm:ss)",
    "termsConditions",
    "couponCode",
    "redeemOnlineUrl",
    "actionUrl",
    "title",
    "privacyLevel (private/public/unlisted)",
    "type (video/short)",
    "privacyLevel (everyone/friends/only_me)",
    "promoteOtherBrand (true/false)",
    "enableComment (true/false)",
    "enableDuet (true/false)",
    "enableStitch (true/false)",
    "videoDisclosure (true/false)",
    "promoteYourBrand (true/false)",
    "title",
    "notifyAllGroupMembers (true/false)",
    "title",
    "link",
]

# Rotating pinned comments (follow-up comment column)
PINNED_COMMENTS = [
    "Love this? I drop daily AI + automation insights at www.skynetjoe.com — come say hi.",
    "Want to build these systems yourself? Grab 47 free tools at skynetlabs-toolkit.vercel.app",
    "My full AI stack + n8n templates are on my GitHub: github.com/waseemnasir2k26",
    "Read the story behind this at www.waseemnasir.com — the origin of SkynetJoe.",
]


def next_slot(date: datetime, times_by_weekday: dict) -> datetime:
    """Return the datetime for the given date at that weekday's slot time."""
    weekday_name = date.strftime("%a")  # Mon, Tue, Wed, ...
    time_str = times_by_weekday.get(weekday_name, "10:00:00")
    h, m, s = [int(x) for x in time_str.split(":")]
    return date.replace(hour=h, minute=m, second=s, microsecond=0)


def build_row(post: dict, when: datetime, image_url: str, pinned: str) -> list:
    content = f"{post['caption']}\n\n{post['hashtags']}"
    youtube_title = post["quote"].replace("\n", " ").strip()[:90]
    pinterest_title = youtube_title
    community_title = youtube_title

    row = [
        when.strftime("%Y-%m-%d %H:%M:%S"),  # 1 postAtSpecificTime
        content,                              # 2 content
        "",                                   # 3 OGmetaUrl
        image_url,                            # 4 imageUrls
        "",                                   # 5 gifUrl
        "",                                   # 6 videoUrls
        "TRUE",                               # 7 mediaOptimization
        "FALSE",                              # 8 applyWatermark
        "ai,motivation,quotes,automation,skynetjoe",  # 9 tags
        "Motivation",                         # 10 category
        pinned,                               # 11 followUpComment
        "post",                               # 12 FB type
        "post",                               # 13 IG type
        "",                                   # 14 LinkedIn pdfTitle
        "FALSE",                              # 15 LinkedIn postAsPdf
        "",                                   # 16 GBP eventType
        "",                                   # 17 GBP actionType
        "",                                   # 18 GBP title
        "",                                   # 19 GBP offerTitle
        "",                                   # 20 GBP startDate
        "",                                   # 21 GBP endDate
        "",                                   # 22 GBP termsConditions
        "",                                   # 23 GBP couponCode
        "",                                   # 24 GBP redeemOnlineUrl
        "",                                   # 25 GBP actionUrl
        youtube_title,                        # 26 YouTube title
        "public",                             # 27 YouTube privacy
        "short",                              # 28 YouTube type
        "everyone",                           # 29 TikTok privacy
        "FALSE",                              # 30 promoteOtherBrand
        "TRUE",                               # 31 enableComment
        "TRUE",                               # 32 enableDuet
        "TRUE",                               # 33 enableStitch
        "FALSE",                              # 34 videoDisclosure
        "FALSE",                              # 35 promoteYourBrand
        community_title,                      # 36 Community title
        "FALSE",                              # 37 notifyAllGroupMembers
        pinterest_title,                      # 38 Pinterest title
        "https://www.skynetjoe.com",          # 39 Pinterest link
    ]
    return row


def main():
    with open(POSTS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    start = datetime.strptime(data["schedule"]["start_date"], "%Y-%m-%d")
    times_by_weekday = data["schedule"]["times_by_weekday"]

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(HEADER_ROW_1)
        writer.writerow(HEADER_ROW_2)

        for i, post in enumerate(data["posts"]):
            date = start + timedelta(days=i)
            when = next_slot(date, times_by_weekday)
            image_url = f"{REPO_RAW_URL}/quote_{post['id']:02d}.png"
            pinned = PINNED_COMMENTS[i % len(PINNED_COMMENTS)]
            row = build_row(post, when, image_url, pinned)
            writer.writerow(row)

    print(f"Wrote {OUT_CSV}")
    print(f"Total rows: {len(data['posts'])}")
    print("Import via GHL > Marketing > Social Planner > Bulk Upload > Advanced.")


if __name__ == "__main__":
    main()
