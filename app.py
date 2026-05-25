"""Sub Verdict — match data is 100% local (match_events.py). Groq only for verdicts."""

from __future__ import annotations

import os
import re
from pathlib import Path

import streamlit as st

from match_events import ALL_MATCHES, MATCH_BY_ID, match_label

# ---------------------------------------------------------------------------
# Config (local match data only — no football-data.org)
# ---------------------------------------------------------------------------

GROQ_MODEL = "llama-3.3-70b-versatile"
VERDICTS = ("Brilliant", "Fine", "Too Late", "Wrong Call")
VERDICT_COLORS = {
    "Brilliant": "#22c55e",
    "Fine": "#eab308",
    "Too Late": "#f97316",
    "Wrong Call": "#ef4444",
}


def _load_env() -> None:
    path = Path(__file__).resolve().parent / ".env"
    if not path.is_file():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def _match_options() -> list[tuple[str, int]]:
    """Dropdown options: (display label, match id). Built from local data only."""
    return [(match_label(m), m["id"]) for m in ALL_MATCHES]


def _sub_button_text(sub: dict) -> str:
    return (
        f"{sub['minute']}' — {sub['playerOut']['name']} → "
        f"{sub['playerIn']['name']} ({sub['scoreline']})"
    )


def _prompt_context(match: dict, sub: dict) -> str:
    ft = match["score"]["fullTime"]
    return (
        f"Match: {match['homeTeam']['name']} vs {match['awayTeam']['name']}\n"
        f"Final score: {ft['home']}-{ft['away']}\n"
        f"Substitution ({sub['minute']}'): {sub['playerOut']['name']} off, "
        f"{sub['playerIn']['name']} on ({sub['team']['name']})\n"
        f"Score at substitution: {sub['scoreline']}"
    )


def _fetch_verdict(context: str) -> tuple[str, str]:
    """Only external HTTP call in this application."""
    from groq import Groq

    key = os.environ.get("GROQ_API_KEY", "")
    if not key or key == "YOUR_KEY_HERE":
        raise ValueError("Set GROQ_API_KEY in .env")

    client = Groq(api_key=key)
    prompt = (
        "You are a sharp football tactics analyst. Judge this Premier "
        "League substitution.\n\n"
        f"{context}\n\n"
        "Reply in exactly this format (verdict must be one of: "
        "Brilliant, Fine, Too Late, Wrong Call):\n"
        "VERDICT: <verdict>\n"
        "EXPLANATION: <2-3 sentences>"
    )
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
    )
    text = response.choices[0].message.content.strip()

    verdict_m = re.search(
        r"VERDICT:\s*(Brilliant|Fine|Too Late|Wrong Call)", text, re.I
    )
    explain_m = re.search(r"EXPLANATION:\s*(.+)", text, re.S | re.I)

    verdict = verdict_m.group(1) if verdict_m else "Fine"
    for v in VERDICTS:
        if verdict.lower() == v.lower():
            verdict = v
            break
    else:
        verdict = "Fine"

    explanation = explain_m.group(1).strip() if explain_m else text
    return verdict, explanation


def _render_verdict(verdict: str, explanation: str) -> None:
    color = VERDICT_COLORS.get(verdict, "#94a3b8")
    st.markdown(
        f"""
        <div style="border-left:6px solid {color};background:{color}22;
            padding:1rem 1.25rem;border-radius:8px;margin-top:0.5rem;">
          <p style="margin:0 0 0.5rem;font-size:1.35rem;font-weight:700;color:{color};">
            {verdict}
          </p>
          <p style="margin:0;color:#e2e8f0;line-height:1.5;">{explanation}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------


def main() -> None:
    _load_env()

    st.set_page_config(page_title="Sub Verdict", page_icon="⚽", layout="centered")
    st.title("Sub Verdict")
    st.caption("Premier League subs · local match data · AI verdicts on demand")

    options = _match_options()
    labels = [label for label, _ in options]
    ids_by_label = {label: mid for label, mid in options}

    choice = st.selectbox("Select a match", labels)
    match_id = ids_by_label[choice]

    if st.session_state.get("_match_id") != match_id:
        st.session_state._match_id = match_id
        st.session_state.pop("verdict", None)

    match = MATCH_BY_ID[match_id]

    st.subheader(choice)
    st.markdown("**Substitutions** — click one for a verdict")

    for i, sub in enumerate(match["substitutions"]):
        btn_label = _sub_button_text(sub)
        if st.button(btn_label, key=f"sub_{match_id}_{i}", use_container_width=True):
            with st.spinner("Getting verdict…"):
                try:
                    v, expl = _fetch_verdict(_prompt_context(match, sub))
                    st.session_state.verdict = {
                        "label": btn_label,
                        "verdict": v,
                        "explanation": expl,
                    }
                except Exception as err:
                    st.error(str(err))
                    st.session_state.pop("verdict", None)

    saved = st.session_state.get("verdict")
    if saved:
        st.divider()
        st.markdown(f"**{saved['label']}**")
        _render_verdict(saved["verdict"], saved["explanation"])


if __name__ == "__main__":
    main()
