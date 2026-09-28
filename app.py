import streamlit as st
from src.models import generate_scorecard

st.set_page_config(page_title="SignalIQ", page_icon="📊", layout="centered")

st.title("SignalIQ")
st.subheader("Meta Ads Signal Intelligence Engine")
st.write("Pre-Launch Scorecard for your campaigns")

if st.button("Generate Pre-Launch Scorecard", type="primary"):
    with st.spinner("Analyzing signals..."):
        result = generate_scorecard()
    
    st.success("Scorecard Ready!")
    
    # Big Score
    st.metric("Readiness Score", f"{result['readiness_score']}/100")
    
    st.divider()
    
    st.subheader("Recommended Actions")
    for i, rec in enumerate(result["recommendations"], 1):
        st.write(f"**{i}.** {rec}")
    
    st.divider()
    
    st.subheader("Details")
    st.write("**Best Hours to Post:**")
    for h in result["best_hours"]:
        st.write(f"- {h['hour']}:00 (score: {round(h['score'], 2)})")
    
    st.write(f"**Top Creative Format:** {result['best_creative']['creative_format']}")
