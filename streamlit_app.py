# dashboard.py
# Streamlit front-end for FastAPI ad-rewriter + two helper endpoints
# Compatible with:
#   • /add_rewriter  – returns {"state": {...}}  OR  {"response": "..."}
#   • /slogan_analyzer (POST {"query": str})
#   • /analyze        (POST {"query": str})

import streamlit as st
import requests
from typing import Dict, Any

# ========== EDIT THESE IF YOUR HOST / PORT DIFFER ========== #
API_BASE = "http://localhost:8000"
REWRITER = f"{API_BASE}/add_rewriter"
SLOGAN   = f"{API_BASE}/slogan_analyzer"
ANALYZE  = f"{API_BASE}/analyze"
TIMEOUT  = 300          # seconds
# ============================================================ #

st.set_page_config(
    page_title="Ad-Tech NLP Console",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.title("Ad-Tech NLP Console 🚀")

# ------------------------------------------------------------------#
# Helper – resilient POST wrapper                                    #
# ------------------------------------------------------------------#
def post(endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any] | None:
    """
    Sends POST, handles 200/4xx, unwraps {"state": {...}}, maps {"response": "..."}
    into the expected key polished_ad.
    """
    try:
        with st.spinner("Calling backend…"):
            resp = requests.post(endpoint, json=payload, timeout=TIMEOUT)
        resp.raise_for_status()
        data = resp.json()

        # ❶ unwrap LangGraph-style {"state": {...}}
        if isinstance(data, dict) and "state" in data and isinstance(data["state"], dict):
            data = data["state"]

        # ❷ map "response" (simple backend) → polished_ad
        if "response" in data and "polished_ad" not in data:
            data["polished_ad"] = data.pop("response")

        return data
    except Exception as e:
        st.error(f"❌ Backend error: {e}")
        return None

# ------------------------------------------------------------------#
# Tabs: 1) Rewriter  2) Slogan  3) Analyze                           #
# ------------------------------------------------------------------#
tab_rw, tab_slogan, tab_analyze = st.tabs(
    ["✏️ Ad Rewriter (loop)", "💡 Slogan Analyzer", "🧐 Deep  research"]
)

# ================================================================ #
# 1) Ad Rewriter tab                                               #
# ================================================================ #

with tab_rw:
    st.header("Iterative Ad Rewriter")

    # ---------- Input form ---------------------------------------#
    with st.form("rewriter_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            tone = st.selectbox("Tone", ["fun", "professional", "witty", "serious",
                                         "bold", "minimal"])
        with col2:
            platform = st.selectbox("Platform", ["Instagram", "Twitter", "LinkedIn",
                                                 "Facebook", "Google Ads", "WhatsApp"])
        initial_ad = st.text_area(
            "Initial Ad Text",
            value="Buy our shoes — you get better quality!",
            height=120,
        )
        submitted = st.form_submit_button("Polish Ad 🚀")

    # ---------- Session storage ----------------------------------#
    if "rw_state" not in st.session_state:
        st.session_state.rw_state = None
    if "rw_history" not in st.session_state:
        st.session_state.rw_history = []

    # ---------- First call ---------------------------------------#
    if submitted and initial_ad.strip():
        st.session_state.rw_history = []   # reset history
        st.session_state.rw_state = {
            "initial_ad": initial_ad,
            "tone": tone,
            "platform": platform,
            "polished_ad": "",
            "is_ok": False,
            "feed_back": ""
        }
        resp = post(REWRITER, st.session_state.rw_state)
        if resp:
            st.session_state.rw_state = resp
            st.session_state.rw_history.append({
                "round": 1,
                "polished_ad": resp.get("polished_ad", ""),
                "feedback": ""
            })

    # ---------- Display + Feedback loop --------------------------#
    state = st.session_state.get("rw_state")
    if state:
        st.subheader("Polished Ad (latest)")
        st.info(state.get("polished_ad", "⚠️ Backend didn’t return polished_ad"))

        with st.container(border=True):
            approve = st.radio(
                "Is this ad ready?",
                ["Needs more work ❌", "Looks perfect ✅"],
                horizontal=True,
                index=0,
                key=f"approve_{len(st.session_state.rw_history)}"
            )

            if approve == "Looks perfect ✅":
                st.success("🎉 Ad approved and ready to publish!")
            else:
                feedback = st.text_area("Your feedback to improve it",
                                        key=f"fb_{len(st.session_state.rw_history)}")
                if st.button("Re-polish with feedback",
                             key=f"rep_{len(st.session_state.rw_history)}"):
                    state["is_ok"] = False
                    state["feed_back"] = feedback
                    resp = post(REWRITER, state)
                    if resp:
                        st.session_state.rw_state = resp
                        st.session_state.rw_history.append({
                            "round": len(st.session_state.rw_history) + 1,
                            "polished_ad": resp.get("polished_ad", ""),
                            "feedback": feedback
                        })
                        st.experimental_rerun()

        # ---------- History --------------------------------------#
        if st.session_state.rw_history:
            st.divider()
            st.subheader("Revision History")
            for item in st.session_state.rw_history:
                st.markdown(f"**Round {item['round']}**")
                st.write(item["polished_ad"] or "—")
                if item["feedback"]:
                    st.caption(f"Feedback: {item['feedback']}")
                st.markdown("---")

# ================================================================ #
# 2) Slogan Analyzer tab                                           #
# ================================================================ #


with tab_slogan:
    st.header("Slogan dataframe Analyzer")
    slogan = st.text_area("Enter a slogan:", height=80, value="what are the top 3 slogans used by amazon. Use the dataframe to help me")
    if st.button("Use the dataframe to help me"):
        res = post(SLOGAN, {"query": slogan})
        if res is not None:
            st.success("Backend response:")
            st.json(res)

# ================================================================ #
# 3) Generic Analyze tab                                           #
# ================================================================ #
with tab_analyze:
    st.header("Deep Research in TECH")
    text = st.text_area("Tech to analyze:", height=120,
                        value="Research deep on the Q3 of apple 2024 sales")
    if st.button("Run /analyze"):
        res = post(ANALYZE, {"query": text})
        if res is not None:
            st.success("Backend response:")
            st.json(res)

# ------------------------------------------------------------------#
st.caption("Streamlit + FastAPI Demo")
