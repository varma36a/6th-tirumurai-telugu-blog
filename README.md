# 6th Tirumurai — Telugu Translation Blog

Translate your **500-page original book** page by page into:

| File | Purpose |
|------|---------|
| `pronunciation.md` | Tamil pronunciation written in Telugu script |
| `telugu.md` | Telugu meaning |

Keep the Tamil original in your book — this repo stores only your translations.

## Setup

```bash
cd /Users/RohithGVMac/Spiritual/6th-tirumurai-telugu-blog
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/init_pages.py
streamlit run app.py
```

## Translate one book page

Edit files in `content/page_NNN/` (001 to 500):

```
content/page_042/
├── meta.json
├── pronunciation.md
└── telugu.md
```

Update `meta.json` title if you want a hymn name in the sidebar:

```json
{
  "book_page": 42,
  "title": "Page 42",
  "notes": ""
}
```

Refresh the Streamlit app after saving.

## Deploy

Push to GitHub and deploy on [Streamlit Community Cloud](https://share.streamlit.io) with main file `app.py`.

Repository: https://github.com/varma36a/6th-tirumurai-telugu-blog
