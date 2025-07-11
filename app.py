# app.py

import streamlit as st
import google.generativeai as genai

# ------------------
# Gemini API Setup
# ------------------
genai.configure(api_key="YOUR_GEMINI_API_KEY")  # ⬅️ Replace with your key

model = genai.GenerativeModel("gemini-pro")

# ------------------
# Streamlit UI
# ------------------
st.set_page_config(page_title="PoliCraft", layout="centered")
st.title("🧠 PoliCraft – AI Policy Assistant")

st.markdown("Craft smarter public policy drafts & simulate stakeholder reactions in seconds.")

# --- Inputs
topic = st.text_input("🔍 Policy Topic", placeholder="e.g., Reduce school dropout rate in Bihar")
sector = st.selectbox("🏛️ Select Sector", ["Education", "Health", "Environment", "Employment", "Agriculture", "Other"])
location = st.text_input("📍 Target Region (optional)", placeholder="e.g., Bihar, India")

# ------------------
# Policy Draft Prompt
# ------------------
def generate_policy(topic, sector, location):
    prompt = f"""
You are a public policy consultant. Draft a concise policy proposal (600 words max) to address the issue:
"{topic}" in the context of {sector} sector {f"in {location}" if location else ""}.

Structure it as follows:
1. Problem Statement
2. Current Landscape
3. Objectives
4. Proposed Interventions
5. Implementation Strategy
6. Risk Factors
7. Budget Estimate (indicative)
8. Key Stakeholders
The tone should be professional, neutral, and suitable for public sector reports in India.
"""
    response = model.generate_content(prompt)
    return response.text

# ------------------
# Stakeholder Prompt
# ------------------
def simulate_stakeholders(policy_draft):
    sim_prompt = f"""
Given the following policy draft:

\"\"\"
{policy_draft}
\"\"\"

Simulate realistic reactions from these stakeholders:
1. Bureaucrat (focus on implementation feasibility)
2. Local citizen (focus on ground impact)
3. Politician (opposition party)
4. NGO worker
5. Supreme Court judge (if applicable)

Each response should reflect the stakeholder's likely perspective in 4–5 sentences.
"""
    sim_response = model.generate_content(sim_prompt)
    return sim_response.text

# ------------------
# App Buttons
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
            sim = simulate_stakeholders(st.session_state["draft"])
            st.subheader("👥 Stakeholder Responses")
            st.markdown(sim)
