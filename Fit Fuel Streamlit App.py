# import streamlit as st
# import google.generativeai as genai
# from reportlab.platypus import SimpleDocTemplate, Paragraph
# from reportlab.lib.styles import getSampleStyleSheet
# from io import BytesIO

# # ---------------- Page Config ----------------
# st.set_page_config(
#     page_title="FitFuel: AI Fitness Coach",
#     layout="centered"
# )

# # ---------------- Gemini Configuration ----------------
# genai.configure(api_key=st.secrets.get("GOOGLE_API_KEY", ""))
# model = genai.GenerativeModel("gemini-2.5-flash")

# # ---------------- Session State ----------------
# if "plan" not in st.session_state:
#     st.session_state.plan = None

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # ---------------- Title ----------------
# st.title("🏋️‍♂️ FitFuel: Your AI Fitness Coach")
# st.write(
#     "Welcome to your **AI Fitness Coach**! 💪  \n"
#     "Get a personalized workout & meal plan, then chat with me to refine it."
# )

# st.divider()

# # ---------------- User Input Form ----------------
# with st.form("fitness_form"):
#     st.subheader("📋 Your Fitness Details")

#     fitness_goal = st.selectbox(
#         "🎯 Fitness Goal",
#         ["Lose Weight", "Build Muscle", "Maintain Fitness", "Improve Endurance"]
#     )

#     weekly_workouts = st.slider(
#         "🏃 Weekly Workouts (days/week)", 1, 7, 3
#     )

#     dietary_preference = st.selectbox(
#         "🥗 Dietary Preference",
#         ["No Preference", "Vegetarian", "Vegan", "Keto", "High-Protein", "Carbs"]
#     )

#     submitted = st.form_submit_button("🚀 Generate My Plan")

# # ---------------- AI Plan Generator ----------------
# def generate_fitness_plan(goal, workouts, diet):
#     prompt = f"""
# You are a professional AI fitness coach.

# Create a personalized fitness plan including:
# 1. Weekly workout schedule
# 2. Simple meal guidance
# 3. Actionable fitness tips

# User profile:
# - Goal: {goal}
# - Workouts per week: {workouts}
# - Diet: {diet}

# Format clearly using markdown headers and bullet points.
# """
#     response = model.generate_content(prompt)
#     return response.text

# # ---------------- Generate Plan ----------------
# if submitted:
#     with st.spinner("Generating your AI fitness plan..."):
#         try:
#             st.session_state.plan = generate_fitness_plan(
#                 fitness_goal, weekly_workouts, dietary_preference
#             )
#             st.session_state.messages = []  # reset chat
#         except Exception as e:
#             st.error(e)

# # ---------------- Display Plan ----------------
# if st.session_state.plan:
#     st.subheader("📘 Your Personalized Plan")
#     st.markdown(st.session_state.plan)

#     st.divider()

#     # ---------------- Chat Mode ----------------
#     st.subheader("💬 Chat with Your AI Coach")

#     # Display chat history
#     for msg in st.session_state.messages:
#         with st.chat_message(msg["role"]):
#             st.markdown(msg["content"])

#     # ---- Chat Input (INTEGRATED CODE) ----
#     if prompt := st.chat_input("Ask a follow-up about your fitness plan..."):

#         # User message
#         st.session_state.messages.append({
#             "role": "user",
#             "content": prompt
#         })
#         st.chat_message("user").write(prompt)

#         # AI response with plan context
#         full_prompt = f"""
# You are an AI fitness coach.

# Here is the user's current fitness plan:
# {st.session_state.plan}

# User question:
# {prompt}

# Respond clearly, concisely, and safely.
# """

#         with st.spinner("Thinking..."):
#             response = model.generate_content(full_prompt)
#             response_text = response.text

#         st.session_state.messages.append({
#             "role": "assistant",
#             "content": response_text
#         })
#         st.chat_message("assistant").write(response_text)

#         st.rerun()

#     st.divider()

#     # ---------------- PDF Export ----------------
#     def create_pdf(text):
#         buffer = BytesIO()
#         doc = SimpleDocTemplate(buffer)
#         styles = getSampleStyleSheet()
#         story = []

#         for line in text.split("\n"):
#             story.append(Paragraph(line.replace("<", "&lt;"), styles["Normal"]))

#         doc.build(story)
#         buffer.seek(0)
#         return buffer

#     pdf_file = create_pdf(st.session_state.plan)

#     col1, col2 = st.columns(2)

#     with col1:
#         if st.button("🔄 Start Over"):
#             st.session_state.plan = None
#             st.session_state.messages = []
#             st.rerun()

#     with col2:
#         st.download_button(
#             "📄 Download Plan as PDF",
#             pdf_file,
#             file_name="AI_Fitness_Plan.pdf",
#             mime="application/pdf"
#         )

















import streamlit as st
import google.generativeai as genai
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

# ---------------- Page Config ----------------
st.set_page_config(page_title="FitFuel: AI Fitness Coach", layout="centered")

# ---------------- Gemini Configuration ----------------
genai.configure(api_key=st.secrets.get("GOOGLE_API_KEY", ""))
# model = genai.GenerativeModel("gemini-1.5-flash")
model = genai.GenerativeModel("gemini-2.5-flash")

# ---------------- Session State ----------------
if "plan" not in st.session_state:
    st.session_state.plan = None

if "conversation" not in st.session_state:
    st.session_state.conversation = []


# ---------------- Title ----------------
st.title("🏋️‍♂️ FitFuel: Your AI Fitness Coach")
st.write(
    "Welcome to your **AI Fitness Coach**! 💪  \n"
    "Get a personalized workout & meal plan, then chat with me to refine it." 
)

st.divider()

# ---------------- User Input Form ----------------
with st.form("fitness_form"):
    st.subheader("📋 Your Fitness Details")

    fitness_goal = st.selectbox(
        "🎯 Fitness Goal",
        ["Lose Weight", "Build Muscle", "Maintain Fitness", "Improve Endurance"]
    )

    weekly_workouts = st.slider(
        "🏃 Weekly Workouts (days/week)", 1, 7, 3
    )

    dietary_preference = st.selectbox(
        "🥗 Dietary Preference",
        ["No Preference", "Vegetarian", "Vegan", "Keto", "High-Protein", "Carbs"]
    )

    submitted = st.form_submit_button("🚀 Generate My Plan")

# ---------------- AI Plan Generator ----------------
def generate_fitness_plan(goal, workouts, diet):
    prompt = f"""
You are a professional AI fitness coach.

Create a personalized fitness plan including:
1. Weekly workout schedule
2. Simple meal guidance
3. Actionable fitness tips

User profile:
- Goal: {goal}
- Workouts per week: {workouts}
- Diet: {diet}

Format clearly using markdown headers and bullet points.
"""
    response = model.generate_content(prompt)
    return response.text

# ---------------- Generate Plan ----------------
if submitted:
    with st.spinner("Generating your AI fitness plan..."):
        try:
            st.session_state.plan = generate_fitness_plan(
                fitness_goal, weekly_workouts, dietary_preference
            )
            st.session_state.chat = []
        except Exception as e:
            st.error(e)

# ---------------- Display Plan ----------------
if st.session_state.plan:
    st.subheader("📘 Your Personalized Plan")
    st.markdown(st.session_state.plan)

    st.divider()

   # ---------------- Chat Mode ----------------
st.subheader("💬 Chat with Your AI Coach")

# Icons
user_icon_url = "https://cdn-icons-png.flaticon.com/128/1057/1057240.png"
bot_icon_url = "https://cdn-icons-png.flaticon.com/128/8943/8943377.png"

# Chat bubble styling
st.markdown("""
<style>
.user-message {
    background-color: #fafafa;
    padding: 8px;
    border-radius: 6px;
}
.bot-message {
    background-color: #ffffff;
    padding: 8px;
    border-radius: 6px;
}
</style>
""", unsafe_allow_html=True)

# Chat display container
chat_placeholder = st.empty()

with chat_placeholder.container():
    for chat in st.session_state.conversation:
        col1, col2 = st.columns([1, 18])
        with col1:
            st.image(user_icon_url, width=32)
        with col2:
            st.markdown(
                f'<div class="user-message">{chat["user"]}</div>',
                unsafe_allow_html=True
            )

        col1, col2 = st.columns([1, 18])
        with col1:
            st.image(bot_icon_url, width=32)
        with col2:
            st.markdown(
                f'<div class="bot-message">{chat["bot"]}</div>',
                unsafe_allow_html=True
            )

# ---- Input form ----
with st.form("chat_form", clear_on_submit=True):
    user_question = st.text_input(
        "Ask a follow-up question about your plan",
        placeholder="E.g. Can you adjust this for home workouts?"
    )
    send = st.form_submit_button("ASK ME", use_container_width=True)

# ---- Handle submission ----
if send and user_question:
    with st.spinner("Thinking..."):

        chat_prompt = f"""
You are an AI fitness coach.

Here is the user's current fitness plan:
{st.session_state.plan}

User question:
{user_question}

Answer clearly, safely, and concisely.
"""

        response = model.generate_content(chat_prompt).text

        st.session_state.conversation.append({
            "user": user_question,
            "bot": response
        })

    st.rerun()


    st.divider()

    # ---------------- PDF Export ----------------
    def create_pdf(text):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer)
        styles = getSampleStyleSheet()
        story = []

        for line in text.split("\n"):
            story.append(Paragraph(line.replace("<", "&lt;"), styles["Normal"]))

        doc.build(story)
        buffer.seek(0)
        return buffer

    pdf_file = create_pdf(st.session_state.plan)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔄 Start Over"):
            st.session_state.plan = None
            st.session_state.conversation = []
            st.rerun()


    with col2:
        st.download_button(
            "📄 Download Plan as PDF",
            pdf_file,
            file_name="AI_Fitness_Plan.pdf",
            mime="application/pdf"
        )










# import streamlit as st
# import google.generativeai as genai

# # ---------------- Page Config ----------------
# st.set_page_config(
#     page_title="FitFuel: AI Fitness Coach",
#     layout="centered"
# )

# # ---------------- Gemini Configuration ----------------
# # Make sure to set GOOGLE_API_KEY in Streamlit secrets or environment variables
# # Example (local): export GOOGLE_API_KEY="your_api_key"

# genai.configure(api_key=st.secrets.get("GOOGLE_API_KEY", ""))
# # model = genai.GenerativeModel("gemini-1.5-flash")
# model = genai.GenerativeModel("gemini-2.5-flash")

# # ---------------- Session State ----------------
# if "plan" not in st.session_state:
#     st.session_state.plan = None

# # ---------------- Title & Intro ----------------
# st.title("🏋️‍♂️ FitFuel: Your AI Fitness Coach")
# st.write(
#     "Welcome to your **AI Fitness Coach**! 💪\n\n"
#     "I'll help you create **personalized workout and meal plans** based on your goals and preferences. "
#     "Just fill out the details below, and I’ll generate a fitness plan tailored **just for you**." 
# )

# st.divider()

# # ---------------- User Input Form ----------------
# with st.form("fitness_form"):
#     st.subheader("📋 Tell me about yourself")

#     fitness_goal = st.selectbox(
#         "🎯 Fitness Goal",
#         ["Lose Weight", "Build Muscle", "Maintain Fitness", "Improve Endurance"]
#     )

#     weekly_workouts = st.slider(
#         "🏃 Weekly Workouts (days per week)",
#         min_value=1,
#         max_value=7,
#         value=3
#     )

#     dietary_preference = st.selectbox(
#         "🥗 Dietary Preference",
#         ["No Preference", "Vegetarian", "Vegan", "Keto", "High-Protein", "carbs"]
#     )

#     submitted = st.form_submit_button("🚀 Generate My Fitness Plan")

# # ---------------- AI Logic (Gemini) ----------------
# def generate_fitness_plan(goal, workouts, diet):
#     prompt = f"""
# You are a professional AI fitness coach.

# Create a personalized, beginner-friendly fitness plan with:
# - A weekly workout schedule
# - Basic meal guidance (no medical claims)
# - Actionable tips

# User details:
# Fitness goal: {goal}
# Workouts per week: {workouts}
# Dietary preference: {diet}

# Format the response in clean markdown with clear section headers.
# """

#     response = model.generate_content(prompt)
#     return response.text

# # ---------------- Generate & Display Plan ----------------
# if submitted:
#     with st.spinner("🤖 Creating your personalized AI fitness plan..."):
#         try:
#             st.session_state.plan = generate_fitness_plan(
#                 fitness_goal,
#                 weekly_workouts,
#                 dietary_preference
#             )
#         except Exception as e:
#             st.error(f"Error generating plan: {e}")

# # ---------------- Output Section ----------------
# if st.session_state.plan:
#     st.divider()
#     st.markdown(st.session_state.plan)

#     col1, col2 = st.columns(2)
#     with col1:
#         if st.button("🔄 Start Over"):
#             st.session_state.plan = None

#     with col2:
#         st.download_button(
#             "📄 Download Plan",
#             st.session_state.plan,
#             file_name="my_ai_fitness_plan.txt"
#         )
