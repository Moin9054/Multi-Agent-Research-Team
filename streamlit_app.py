# streamlit_app.py
"""
Final stable version — no external dependencies.
Modern UI, Markdown rendering, safe client-side copy buttons.
"""

import streamlit as st
import asyncio
import os
import html
import re
from datetime import datetime
from app.agents import run_team

# ---------------- Page Setup ----------------
st.set_page_config(page_title="Multi-Agent Research Team", layout="wide")

# ---------------- CSS ----------------
st.markdown("""
<style>
:root {
  --bg: #f6f8fa;
  --card: #ffffff;
  --muted: #6b7280;
  --accent: #2563eb;
  --radius: 12px;
  --shadow: 0 6px 18px rgba(15,23,42,0.08);
}
body { background: var(--bg); }
.card {
  background: var(--card);
  padding: 22px;
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  margin-bottom: 18px;
}
.header { font-size:2rem; font-weight:800; margin-bottom:4px; }
.subtitle { color:var(--muted); margin-bottom:14px; }
.copy-btn {
  background: #f3f4f6;
  border: none;
  color: var(--muted);
  font-size: 0.9rem;
  padding: 4px 10px;
  border-radius: 8px;
  cursor: pointer;
}
.copy-btn:hover { background: #e5e7eb; color: var(--accent); }
</style>
""", unsafe_allow_html=True)

# ---------------- Helper: clean text ----------------
def clean_output(text: str) -> str:
    if not text:
        return ""
    text = text.replace("\\r\\n", "\n").replace("\\n", "\n").replace("\\r", "\n")
    text = html.unescape(text)
    text = re.sub(r"<script[\s\S]*?</script>", "", text, flags=re.IGNORECASE)
    text = re.sub(r"<style[\s\S]*?</style>", "", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>\n]+>", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text

# ---------------- Helper: Copy button (safe JS) ----------------
def render_copy_button(text: str, btn_id: str):
    js = f"""
    <script>
    function copyToClipboard_{btn_id}() {{
        navigator.clipboard.writeText({repr(text)}).then(() => {{
            const el = document.getElementById("{btn_id}");
            if (el) {{
                el.innerText = "✅ Copied";
                setTimeout(() => el.innerText = "📋 Copy", 1500);
            }}
        }});
    }}
    </script>
    <button id="{btn_id}" class="copy-btn" onclick="copyToClipboard_{btn_id}()">📋 Copy</button>
    """
    st.markdown(js, unsafe_allow_html=True)

# ---------------- Header ----------------
st.markdown('<div class="header">Multi-Agent Research Team</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Enter a topic and run the team (Researcher, Analyst, Strategist, Coordinator).</div>', unsafe_allow_html=True)

# ---------------- Input Section ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)
topic = st.text_input("Topic", value="Impact of Artificial Intelligence on Global Education")
run_clicked = st.button("Run Team 🚀", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

# ---------------- Session State ----------------
if "last_outputs" not in st.session_state:
    st.session_state.last_outputs = None
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- Run Agents ----------------
if run_clicked:
    if not topic.strip():
        st.error("Please enter a topic before running.")
    else:
        with st.spinner("Running agents... please wait ⏳"):
            try:
                outputs = asyncio.run(asyncio.to_thread(run_team, topic))
            except Exception as e:
                st.error(f"Error running team: {e}")
                outputs = None

        if outputs:
            st.session_state.last_outputs = {
                k: clean_output(v) for k, v in outputs.items()
            }
            st.session_state.history.append(
                (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), topic)
            )
        else:
            st.error("No output received.")

# ---------------- Display Results ----------------
if st.session_state.last_outputs:
    data = st.session_state.last_outputs

    # Coordinator summary
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 🧭 Coordinator Summary")
    st.markdown(data.get("coordinator", "_No coordinator output_"))
    render_copy_button(data.get("coordinator", ""), "copy_coord")
    st.markdown('</div>', unsafe_allow_html=True)

    # Other agents
    cols = st.columns(3)
    for i, role in enumerate(["research", "analysis", "strategy"]):
        with cols[i]:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            role_name = role.capitalize()
            st.markdown(f"### {role_name} Output")
            st.markdown(data.get(role, f"_No {role_name} output_"))
            render_copy_button(data.get(role, ""), f"copy_{role}")
            st.markdown('</div>', unsafe_allow_html=True)

# ---------------- History ----------------
if st.session_state.history:
    st.markdown("#### Recent Runs")
    for ts, top in reversed(st.session_state.history[-5:]):
        st.markdown(f"- **{top}** — *{ts}*")
