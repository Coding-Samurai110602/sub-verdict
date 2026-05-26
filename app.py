"""Sub Verdict — local match data; Groq for verdicts only."""

from __future__ import annotations

import base64
import os
import re
import urllib.parse
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from match_events import (
    ALL_MATCHES,
    MATCH_BY_ID,
    crest_url,
    manager_rating,
    match_label,
    what_happened_after,
)

GROQ_MODEL = "llama-3.3-70b-versatile"
VERDICTS = ("Brilliant", "Fine", "Too Late", "Wrong Call")
VERDICT_COLORS = {
    "Brilliant": "#00ff87",
    "Fine": "#eab308",
    "Too Late": "#f97316",
    "Wrong Call": "#ef4444",
}
MASCOT = {
    "Brilliant": "🤩",
    "Fine": "😐",
    "Too Late": "😤",
    "Wrong Call": "🤦",
}

_CSS_BASE = """
<style>
  @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800&display=swap');

  .stApp {
    background: transparent !important;
    color: #e6edf3;
    font-family: 'Outfit', sans-serif;
  }
  [data-testid="stAppViewContainer"] {
    background: transparent !important;
  }
  [data-testid="stHeader"] { background: transparent; }
  [data-testid="stToolbar"] { display: none; }
  .main .block-container {
    padding-top: 1.5rem;
    max-width: 720px;
    background: transparent;
  }

  .sv-bg-wrap {
    position: fixed;
    inset: 0;
    z-index: -1;
    pointer-events: none;
  }
  .sv-bg-image {
    position: absolute;
    inset: 0;
    background-image: url("data:image/jpeg;base64,{bg_b64}");
    background-size: cover;
    background-position: center center;
    background-repeat: no-repeat;
    background-attachment: fixed;
  }
  .sv-bg-overlay {
    position: absolute;
    inset: 0;
    background: rgba(13, 17, 23, 0.75);
  }

  .sv-sub-block {
    margin-bottom: 1.25rem;
    padding-bottom: 0.25rem;
  }
  .sv-sub-card.sv-sub-card-active {
    border-color: #00ff87;
    box-shadow: 0 0 24px #00ff8733;
  }
  .sv-inline-verdict {
    margin-top: 0.75rem;
    padding: 0 0.15rem;
  }

  .sv-header {
    text-align: center;
    padding: 1.5rem 1rem 2rem;
    border-bottom: 1px solid #21262d;
    margin-bottom: 1.5rem;
  }
  .sv-header h1 {
    margin: 0;
    font-size: 2.4rem;
    font-weight: 800;
    color: #00ff87;
    letter-spacing: -0.02em;
  }
  .sv-header p {
    margin: 0.4rem 0 0;
    color: #8b949e;
    font-size: 1.05rem;
  }

  .sv-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 1rem 1.15rem;
    margin-bottom: 0.75rem;
  }
  .sv-card-accent {
    border-color: #00ff8744;
    box-shadow: 0 0 20px #00ff8715;
  }

  .sv-fixture {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    flex-wrap: wrap;
  }
  .sv-fixture-team {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    font-weight: 600;
    font-size: 1.05rem;
  }
  .sv-fixture-team img {
    width: 40px;
    height: 40px;
    object-fit: contain;
  }
  .sv-fixture-score {
    font-size: 1.5rem;
    font-weight: 800;
    color: #00ff87;
    min-width: 4rem;
    text-align: center;
  }
  .sv-fixture-lg img { width: 52px; height: 52px; }
  .sv-fixture-lg .sv-fixture-score { font-size: 1.85rem; }

  .sv-sub-card {
    background: linear-gradient(135deg, #161b22 0%, #1c2128 100%);
    border: 1px solid #30363d;
    border-radius: 14px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.5rem;
    transition: border-color 0.2s, box-shadow 0.2s;
  }
  .sv-sub-card:hover {
    border-color: #00ff87;
    box-shadow: 0 0 24px #00ff8733;
  }
  .sv-sub-minute {
    display: inline-block;
    background: #00ff8722;
    color: #00ff87;
    font-weight: 700;
    padding: 0.2rem 0.55rem;
    border-radius: 6px;
    font-size: 0.85rem;
    margin-bottom: 0.5rem;
  }
  .sv-sub-players {
    font-size: 1.05rem;
    font-weight: 600;
    line-height: 1.4;
  }
  .sv-sub-meta {
    color: #8b949e;
    font-size: 0.88rem;
    margin-top: 0.35rem;
  }
  .sv-pos {
    display: inline-block;
    background: #21262d;
    border: 1px solid #30363d;
    color: #8b949e;
    font-size: 0.72rem;
    font-weight: 700;
    padding: 0.1rem 0.35rem;
    border-radius: 4px;
    margin: 0 0.15rem;
  }

  .sv-verdict {
    border-left: 6px solid #2d6a4f;
    background: #161b22;
    border-radius: 0 12px 12px 0;
    padding: 1.25rem 1.35rem;
    margin: 1rem 0;
    border-top: 1px solid #30363d;
    border-right: 1px solid #30363d;
    border-bottom: 1px solid #30363d;
  }
  .sv-verdict-title {
    font-size: 1.45rem;
    font-weight: 800;
    margin: 0 0 0.5rem;
  }
  .sv-verdict-body {
    color: #c9d1d9;
    line-height: 1.55;
    margin: 0;
  }

  .sv-mascot {
    font-size: 5rem;
    text-align: center;
    margin: 0.5rem 0 1rem;
    animation: sv-bounce 1.2s ease infinite;
  }
  @keyframes sv-bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-14px); }
  }

  .sv-fact {
    background: #0d1117;
    border: 1px dashed #30363d;
    border-radius: 10px;
    padding: 0.9rem 1rem;
    margin-top: 0.75rem;
  }
  .sv-fact h4 {
    margin: 0 0 0.35rem;
    color: #00ff87;
    font-size: 0.95rem;
  }
  .sv-fact p { margin: 0; color: #8b949e; font-size: 0.9rem; }

  .sv-poll-bar {
    height: 10px;
    border-radius: 5px;
    overflow: hidden;
    display: flex;
    margin: 0.5rem 0;
    background: #21262d;
  }
  .sv-poll-agree { background: #00ff87; }
  .sv-poll-disagree { background: #f85149; }

  .sv-manager {
    text-align: center;
    padding: 1.25rem;
  }
  .sv-manager-score {
    font-size: 3.5rem;
    font-weight: 800;
    line-height: 1;
    margin: 0.25rem 0;
  }
  .sv-manager-label {
    color: #8b949e;
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
  }

  .sv-tweet-btn {
    display: block;
    text-align: center;
    background: rgba(29, 161, 242, 0.15);
    color: #1da1f2 !important;
    border: 1px solid #1da1f2;
    padding: 0.6rem 1.2rem;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
    text-decoration: none !important;
    font-size: 0.95rem;
  }
  .sv-tweet-btn:hover { background: rgba(29, 161, 242, 0.25); }

  div[data-testid="stButton"] > button {
    background: linear-gradient(180deg, #238636 0%, #196c2e 100%);
    color: #fff;
    border: 1px solid #2ea043;
    border-radius: 10px;
    font-weight: 600;
    transition: box-shadow 0.2s, transform 0.15s;
  }
  div[data-testid="stButton"] > button:hover {
    box-shadow: 0 0 20px #00ff8755;
    border-color: #00ff87;
    transform: translateY(-1px);
  }
  div[data-testid="stButton"] > button[kind="secondary"] {
    background: #21262d;
    border-color: #30363d;
  }
  div[data-testid="stButton"] > button[kind="secondary"]:hover {
    box-shadow: 0 0 16px #f8514933;
    border-color: #8b949e;
  }

  [data-testid="stSelectbox"] label { color: #8b949e !important; }
  .stSelectbox > div > div {
    background: #161b22;
    border-color: #30363d;
    color: #e6edf3;
  }
</style>
"""


def _background_css() -> str:
    bg_path = Path(__file__).resolve().parent / "background.jpg"
    bg_b64 = ""
    if bg_path.is_file():
        bg_b64 = base64.b64encode(bg_path.read_bytes()).decode("ascii")
    return _CSS_BASE.replace("{bg_b64}", bg_b64)


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


def _fixture_html(match: dict, large: bool = False) -> str:
    ft = match["score"]["fullTime"]
    home = match["homeTeam"]
    away = match["awayTeam"]
    lg = " sv-fixture-lg" if large else ""
    return f"""
    <div class="sv-fixture{lg}">
      <div class="sv-fixture-team">
        <img src="{crest_url(home['id'])}" alt="{home['shortName']}" />
        <span>{home['shortName']}</span>
      </div>
      <div class="sv-fixture-score">{ft['home']} – {ft['away']}</div>
      <div class="sv-fixture-team">
        <img src="{crest_url(away['id'])}" alt="{away['shortName']}" />
        <span>{away['shortName']}</span>
      </div>
    </div>
    """


def _sub_card_html(sub: dict, *, active: bool = False) -> str:
    extra = " sv-sub-card-active" if active else ""
    return f"""
    <div class="sv-sub-card{extra}">
      <span class="sv-sub-minute">{sub['minute']}'</span>
      <div class="sv-sub-players">
        {sub['playerOut']['name']}
        <span class="sv-pos">{sub['positionOut']}</span>
        → {sub['playerIn']['name']}
        <span class="sv-pos">{sub['positionIn']}</span>
      </div>
      <div class="sv-sub-meta">
        {sub['team']['shortName']} · Score {sub['scoreline']}
      </div>
    </div>
    """


def _prompt_context(match: dict, sub: dict) -> str:
    ft = match["score"]["fullTime"]
    return (
        f"Match: {match['homeTeam']['name']} vs {match['awayTeam']['name']}\n"
        f"Final score: {ft['home']}-{ft['away']}\n"
        f"Substitution ({sub['minute']}'): {sub['playerOut']['name']} "
        f"({sub['positionOut']}) off, {sub['playerIn']['name']} "
        f"({sub['positionIn']}) on ({sub['team']['name']})\n"
        f"Score at substitution: {sub['scoreline']}"
    )


def _fetch_verdict(context: str) -> tuple[str, str]:
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


def _rating_style(score: float) -> tuple[str, str]:
    if score > 7:
        return "#00ff87", "Strong bench management"
    if score >= 5:
        return "#eab308", "Mixed decisions"
    return "#f85149", "Subs struggled to land"


def _active_sub_key(match_id: int, sub_idx: int) -> str:
    return f"{match_id}_{sub_idx}"


def _verdict_data_key(match_id: int, sub_idx: int) -> str:
    return f"verdict_data_{match_id}_{sub_idx}"


def _poll_key(match_id: int, sub_idx: int) -> str:
    return f"poll_{match_id}_{sub_idx}"


def _init_poll(key: str) -> None:
    if key not in st.session_state:
        st.session_state[key] = {"agree": 0, "disagree": 0, "user_vote": None}


def _render_inline_verdict(match: dict, match_id: int, sub_idx: int, data: dict) -> None:
    sub = data["sub"]
    verdict = data["verdict"]
    color = VERDICT_COLORS.get(verdict, "#00ff87")
    after = what_happened_after(match, sub)

    tweet_text = (
        f"🔴 {verdict.upper()} — {sub['team']['shortName']} pulled "
        f"{sub['playerOut']['name']} ({sub['positionOut']}) for "
        f"{sub['playerIn']['name']} ({sub['positionIn']}) at {sub['minute']}' "
        f"({sub['scoreline']}). #SubVerdict #PremierLeague"
    )
    tweet_url = "https://twitter.com/intent/tweet?text=" + urllib.parse.quote(tweet_text)

    poll_key = _poll_key(match_id, sub_idx)
    _init_poll(poll_key)
    poll = st.session_state[poll_key]
    user_voted = poll["user_vote"] is not None

    st.markdown('<div class="sv-inline-verdict">', unsafe_allow_html=True)

    # Mascot
    st.markdown(f'<div class="sv-mascot">{MASCOT[verdict]}</div>', unsafe_allow_html=True)

    # Verdict card
    st.markdown(
        f"""
        <div class="sv-verdict">
          <p class="sv-verdict-title" style="color:{color};">{verdict}</p>
          <p class="sv-verdict-body">{data['explanation']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Share section
    st.markdown("#### Share this verdict")
    st.code(tweet_text, language=None)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("📋 Copy to clipboard", key=f"copy_{poll_key}", use_container_width=True):
            components.html(
                f"""<script>navigator.clipboard.writeText({repr(tweet_text)});</script>""",
                height=0,
            )
            st.toast("✅ Copied to clipboard!")
    with c2:
        st.markdown(
            f'<a href="{tweet_url}" target="_blank" class="sv-tweet-btn">Tweet this</a>',
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Fan Poll
    st.markdown("#### Fan poll")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("👍 Agree", key=f"agree_{poll_key}", use_container_width=True):
            if poll["user_vote"] is None:
                poll["agree"] += 1
                poll["user_vote"] = "agree"
                st.rerun()
    with c2:
        if st.button(
            "👎 Disagree",
            key=f"disagree_{poll_key}",
            type="secondary",
            use_container_width=True,
        ):
            if poll["user_vote"] is None:
                poll["disagree"] += 1
                poll["user_vote"] = "disagree"
                st.rerun()

    total = poll["agree"] + poll["disagree"]
    if total > 0:
        agree_pct = int(round(100 * poll["agree"] / total))
        st.markdown(
            f"""
            <div class="sv-poll-bar">
              <div class="sv-poll-agree" style="width:{agree_pct}%"></div>
              <div class="sv-poll-disagree" style="width:{100 - agree_pct}%"></div>
            </div>
            <p style="color:#8b949e;font-size:0.88rem;margin:0;">
              <span style="color:#00ff87;">{agree_pct}% agree</span>
              · {total} vote{"s" if total != 1 else ""}
            </p>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.caption("Be the first to vote on this verdict.")

    # What happened after — revealed only after voting
    if user_voted:
        st.markdown(
            """
            <div style="margin-top:0.75rem;padding:0.6rem 1rem;
            background:#00ff8715;border-radius:8px;color:#00ff87;
            font-size:0.9rem;font-weight:600;">
              You voted! Here's what actually happened...
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
            <div class="sv-fact">
              <h4>{after['icon']} What happened after</h4>
              <p><strong>{after['headline']}</strong> — {after['detail']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)


def main() -> None:
    _load_env()

    st.set_page_config(
        page_title="Sub Verdict",
        page_icon="⚽",
        layout="centered",
        initial_sidebar_state="collapsed",
    )
    st.markdown(_background_css(), unsafe_allow_html=True)
    st.markdown(
        '<div class="sv-bg-wrap"><div class="sv-bg-image"></div>'
        '<div class="sv-bg-overlay"></div></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="sv-header">
          <h1>⚽ Sub Verdict</h1>
          <p>Was that sub the right call?</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    options = [(match_label(m), m["id"]) for m in ALL_MATCHES]
    labels = [label for label, _ in options]
    ids_by_label = {label: mid for label, mid in options}

    st.markdown("##### Select a match")
    choice = st.selectbox(
        "Match",
        labels,
        label_visibility="collapsed",
        format_func=lambda x: x,
    )
    match_id = ids_by_label[choice]
    match = MATCH_BY_ID[match_id]

    if st.session_state.get("_match_id") != match_id:
        st.session_state._match_id = match_id
        st.session_state.active_sub = None

    st.markdown(
        f'<div class="sv-card sv-card-accent sv-fixture-lg">{_fixture_html(match, large=True)}</div>',
        unsafe_allow_html=True,
    )

    st.markdown("##### Substitutions")
    st.caption("Tap a change to get the AI verdict")

    for i, sub in enumerate(match["substitutions"]):
        sub_key = _active_sub_key(match_id, i)
        is_active = st.session_state.get("active_sub") == sub_key

        st.markdown('<div class="sv-sub-block">', unsafe_allow_html=True)
        st.markdown(_sub_card_html(sub, active=is_active), unsafe_allow_html=True)

        if st.button("Get verdict", key=f"btn_{match_id}_{i}", use_container_width=True):
            st.session_state.active_sub = sub_key
            with st.spinner("Analysing the change…"):
                try:
                    verdict, explanation = _fetch_verdict(_prompt_context(match, sub))
                    st.session_state[_verdict_data_key(match_id, i)] = {
                        "verdict": verdict,
                        "explanation": explanation,
                        "sub": sub,
                    }
                    st.rerun()
                except Exception as err:
                    st.error(str(err))
                    st.session_state.pop(_verdict_data_key(match_id, i), None)
                    if st.session_state.get("active_sub") == sub_key:
                        st.session_state.active_sub = None

        is_active = st.session_state.get("active_sub") == sub_key
        if is_active:
            saved = st.session_state.get(_verdict_data_key(match_id, i))
            if saved and saved.get("sub"):
                _render_inline_verdict(match, match_id, i, saved)

        st.markdown("</div>", unsafe_allow_html=True)

    rating = manager_rating(match)
    r_color, r_note = _rating_style(rating)
    st.markdown(
        f"""
        <div class="sv-card sv-manager" style="margin-top:1.5rem;">
          <p class="sv-manager-label">Manager rating</p>
          <p class="sv-manager-score" style="color:{r_color};">{rating}</p>
          <p style="color:#8b949e;margin:0;font-size:0.95rem;">out of 10 · {r_note}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()