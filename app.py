# app.py

import streamlit as st
import os
import google.generativeai as genai

# ------------------
# API Setup
# ------------------
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Use Gemini Pro (correct model name)
model = genai.GenerativeModel(model_name="models/gemini-pro")

# ------------------
# Streamlit UI Setup
# ------------------
st.set_page_config(page_title="PoliCraft", layout="centered")
st.title("🧠 PoliCraft – AI Policy Assistant")
st.markdown("Craft smarter public policy drafts & simulate stakeholder reactions in seconds.")

# ------------------
# User Inputs
# ------------------
topic = st.text_input("🔍 Policy Topic", placeholder="e.g., Reduce school dropout rate in Bihar")
sector = st.selectbox("🏛️ Select Sector", ["Education", "Health", "Environment", "Employment", "Agriculture", "Other"])
location = st.text_input("📍 Target Region (optional)", placeholder="e.g., Bihar, India")

# ------------------
# Policy Draft Function
# ------------------
def generate_policy(topic, sector, location):
    prompt = f"""
You are a public policy consultant. Draft a concise policy proposal (max 600 words) to address:
"{topic}" in the {sector} sector {f"in {location}" if location else ""}.

Structure:
1. Problem Statement
2. Current Landscape
3. Objectives
4. Proposed Interventions
5. Implementation Strategy
6. Risk Factors
7. Budget Estimate (indicative)
8. Key Stakeholders

Tone: Formal, professional, and suitable for an Indian policy audience.
"""
    try:
        response = model.generate_content([prompt])
        return response.text
    except Exception as e:
        return f"❌ Error: {e}"

# ------------------
# Stakeholder Simulation Function
# ------------------
def simulate_stakeholders(policy_draft):
    prompt = f"""
Given the following policy draft:

\"\"\"
{policy_draft}
\"\"\"

Simulate realistic reactions from:
1. Bureaucrat (implementation feasibility)
2. Local Citizen (impact on daily life)
3. Opposition Politician (political critique)
4. NGO Worker (sustainability and inclusiveness)
5. Supreme Court Judge (legal/constitutional aspects)

Each response should be 4–5 sentences.
"""
    try:
        response = model.generate_content([prompt])
        return response.text
    except Exception as e:
        return f"❌ Error: {e}"

# ------------------
# UI Actions
# ------------------
if st.button("🚀 Generate Policy Draft"):
    if topic.strip():
        with st.spinner("Generating policy draft..."):
            draft = generate_policy(topic, sector, location)
            st.subheader("📄 Policy Draft")
            st.markdown(draft)
            st.session_state["draft"] = draft
    else:
        st.warning("Please enter a policy topic.")

if "draft" in st.session_state:
    if st.button("🤝 Simulate Stakeholder Reactions"):
        with st.spinner("Simulating reactions..."):
            reactions = simulate_stakeholders(st.session_state["draft"])
            st.subheader("👥 Stakeholder Reactions")
            st.markdown(reactions)
