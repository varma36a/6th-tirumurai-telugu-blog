# 6th Tirumurai — Telugu Translation Blog

Streamlit blog for the **[Sixth Thirumurai](https://www.thiruarutpa.org/Thirumurai/sixth/tm)** (Thirunavukkarasar / Appar Swami):

| Column | File | Source |
|--------|------|--------|
| Tamil | `tamil.md` | [thiruarutpa.org](https://www.thiruarutpa.org/Thirumurai/sixth/tm) |
| Pronunciation | `pronunciation.md` | You add — Tamil sounds in Telugu script |
| Telugu | `telugu.md` | You add — Telugu meaning / translation |

## Run locally

```bash
cd /Users/RohithGVMac/Spiritual/6th-tirumurai-telugu-blog
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Import / refresh Tamil text from thiruarutpa.org

```bash
python scripts/import_from_thiruarutpa.py
```

This creates 150 folders under `content/` (one per path on the site). Existing Telugu/pronunciation files are kept.

## Add Telugu for one path

Edit these files in the matching folder, e.g. `content/001_parasiva_vanakkam/`:

- `pronunciation.md`
- `telugu.md`

Refresh the Streamlit app — no code changes needed.

## Deploy

Push to GitHub, then deploy on [Streamlit Community Cloud](https://share.streamlit.io) with main file `app.py`.

## Source

- Index: https://www.thiruarutpa.org/Thirumurai/sixth/tm
- Each page stores its direct `source_url` in `meta.json`
