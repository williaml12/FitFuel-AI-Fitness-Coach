import streamlit as st
import google.generativeai as genai

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="FitFuel: AI Fitness Coach",
    layout="centered"
)

# ---------------- Gemini Configuration ----------------
# Make sure to set GOOGLE_API_KEY in Streamlit secrets or environment variables
# Example (local): export GOOGLE_API_KEY="your_api_key"

api_key = st.secrets["GOOGLE_API_KEY"]
# genai.configure(api_key=st.secrets.get("GOOGLE_API_KEY", ""))
genai.configure(api_key=api_key)
# model = genai.GenerativeModel("gemini-1.5-flash")
model = genai.GenerativeModel("gemini-2.5-flash")

# ---------------- Session State ----------------
if "plan" not in st.session_state:
    st.session_state.plan = None

# ---------------- Title & Intro ----------------
st.title("🏋️‍♂️ FitFuel: Your AI Fitness Coach")
st.write(
    "Welcome to your **AI Fitness Coach**! 💪\n\n"
    "I'll help you create **personalized workout and meal plans** based on your goals and preferences. "
    "Just fill out the details below, and I’ll generate a fitness plan tailored **just for you**." 
)

st.divider()

# ---------------- User Input Form ----------------
with st.form("fitness_form"):
    st.subheader("📋 Tell me about yourself")

    fitness_goal = st.selectbox(
        "🎯 Fitness Goal",
        ["Lose Weight", "Build Muscle", "Maintain Fitness", "Improve Endurance"]
    )

    weekly_workouts = st.slider(
        "🏃 Weekly Workouts (days per week)",
        min_value=1,
        max_value=7,
        value=3
    )

    dietary_preference = st.selectbox(
        "🥗 Dietary Preference",
        ["No Preference", "Vegetarian", "Vegan", "Keto", "High-Protein"]
    )

    submitted = st.form_submit_button("🚀 Generate My Fitness Plan")

# ---------------- AI Logic (Gemini) ----------------
def generate_fitness_plan(goal, workouts, diet):
    prompt = f"""
You are a professional AI fitness coach.

Create a personalized, beginner-friendly fitness plan with:
- A weekly workout schedule
- Basic meal guidance (no medical claims)
- Actionable tips

User details:
Fitness goal: {goal}
Workouts per week: {workouts}
Dietary preference: {diet}

Format the response in clean markdown with clear section headers.
"""

    response = model.generate_content(prompt)
    return response.text

# ---------------- Generate & Display Plan ----------------
if submitted:
    with st.spinner("🤖 Creating your personalized AI fitness plan..."):
        try:
            st.session_state.plan = generate_fitness_plan(
                fitness_goal,
                weekly_workouts,
                dietary_preference
            )
        except Exception as e:
            st.error(f"Error generating plan: {e}")

# ---------------- Output Section ----------------
if st.session_state.plan:
    st.divider()
    st.markdown(st.session_state.plan)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Start Over"):
            st.session_state.plan = None

    with col2:
        st.download_button(
            "📄 Download Plan",
            st.session_state.plan,
            file_name="my_ai_fitness_plan.txt"
        )
