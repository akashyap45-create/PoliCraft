# app.py

import streamlit as st
import os
import google.generativeai as genai

# ------------------
# API Setup
# ------------------
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use Gemini 1.5 Pro (latest version, correct model name)
model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")

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
# Policy Draft Prompt
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
    response = model.generate_content([prompt])
    return response.text

# ------------------
# Stakeholder Simulation Prompt
# ------------------
def simulate_stakeholders(policy_draft):
    prompt = f"""
Given the following policy draft:

\"\"\"
{policy_draft}
\"\"\"

Simulate reactions from:
1. Bureaucrat (focus on implementation feasibility)
2. Local Citizen (focus on ground-level impact)
3. Opposition Politician (focus on political concerns)
4. NGO Worker (focus on inclusiveness and sustainability)
5. Supreme Court Judge (legal and constitutional aspects, if applicable)

Each response should be 4–5 sentences and reflect their realistic viewpoints.
"""
    response = model.generate_content([prompt])
    return response.text

# ------------------
# Generate Policy Draft
# ------------------
if st.button("🚀 Generate Policy Draft"):
    if topic.strip():
        with st.spinner("Generating policy draft..."):
            try:
                draft = generate_policy(topic, sector, location)
                st.subheader("📄 Policy Draft")
                st.markdown(draft)
                st.session_state["draft"] = draft
            except Exception as e:
                st.error(f"Something went wrong: {e}")
    else:
        st.warning("Please enter a policy topic.")

# ------------------
# Simulate Stakeholder Reactions
# ------------------
if "draft" in st.session_state:
    if st.button("🤝 Simulate Stakeholder Reactions"):
        with st.spinner("Simulating responses..."):
            try:
                sim = simulate_stakeholders(st.session_state["draft"])
                st.subheader("👥 Stakeholder Reactions")
                st.markdown(sim)
            except Exception as e:
                st.error(f"Simulation failed: {e}")

