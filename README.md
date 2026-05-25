# Sub Verdict ⚽

> AI-powered Premier League substitution analyzer — was that sub the right call?

## What it does

Sub Verdict lets football fans instantly judge manager decisions. Pick a recent Premier League match, click any substitution, and get an AI-powered verdict:

- 🟢 **Brilliant** — textbook decision
- 🟡 **Fine** — reasonable but nothing special
- 🟠 **Too Late** — should have acted earlier
- 🔴 **Wrong Call** — questionable decision with explanation

## Live Demo

👉 [sub-verdict-ej75xyjqutdcnz8h7tukug.streamlit.app](https://sub-verdict-ej75xyjqutdcnz8h7tukug.streamlit.app/)

## Tech Stack

- **Frontend:** Streamlit
- **AI:** Groq LLaMA 3.3 70B
- **Data:** Hardcoded Premier League 2025/26 match events

## Run Locally

```bash
git clone https://github.com/Coding-Samurai110602/sub-verdict.git
cd sub-verdict
pip install -r requirements.txt
```

Create a `.env` file:
GROQ_API_KEY=your_groq_api_key

Then run:
```bash
streamlit run app.py
```

## Built at

Cursor Boston Sports Hack 2026 — Boston Tech Week
