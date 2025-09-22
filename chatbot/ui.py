import streamlit as st
from chatbot.llm import is_tech_stack_relevant, generate_questions
from chatbot.data_handler import save_interview_to_excel

def render_candidate_info_form():
    with st.form("candidate_info_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number")
        experience = st.number_input("Years of Experience", 0, 50, 1)
        position = st.text_input("Desired Position(s)")
        location = st.text_input("Current Location")
        tech_stack = st.text_area("Tech Stack (comma separated)")
        submitted = st.form_submit_button("Submit")
        if submitted:
            if not (name.strip() and email.strip() and tech_stack.strip()):
                st.warning("Please fill at least Name, Email, and Tech Stack.")
                return None

            if not is_tech_stack_relevant(tech_stack):
                st.warning(
                    "Your tech stack does not seem relevant. Please enter a proper tech stack like Python, React, Java."
                )
                return None

            techs = [t.strip() for t in tech_stack.split(",") if t.strip()]

            return {
                "name": name.strip(),
                "email": email.strip(),
                "phone": phone.strip(),
                "experience": experience,
                "position": position.strip(),
                "location": location.strip(),
                "tech_stack": techs,
            }
    return None


def render_ui():
    exit_input = st.text_input("Type 'exit' anytime to quit.", key="exit_input")
    if exit_input.strip().lower() in ("exit", "quit", "bye"):
        st.write("Thank you for visiting TalentScout. Goodbye!")
        st.stop()

    if st.session_state.step == "greet":
        st.title("TalentScout Hiring Assistant Chatbot")
        st.write("Welcome! Let's get started.")
        if st.button("Start Interview"):
            st.session_state.step = "collect_info"
            st.rerun()

    elif st.session_state.step == "collect_info":
        info = render_candidate_info_form()
        if info:
            st.session_state.candidate_info = info
            st.session_state.step = "generate_questions"
            st.rerun()

    elif st.session_state.step == "generate_questions":
        st.write("Generating questions...")
        tech_stack = st.session_state.candidate_info.get("tech_stack", [])
        st.session_state.questions = generate_questions(tech_stack)
        st.session_state.answers = []
        st.session_state.current_q_index = 0
        st.session_state.step = "ask_questions"
        st.rerun()

    elif st.session_state.step == "ask_questions":
        idx = st.session_state.current_q_index
        if idx >= len(st.session_state.questions):
            st.session_state.step = "summary"
            st.rerun()
            return

        question = st.session_state.questions[idx]
        st.markdown(f"### Question {idx+1} of {len(st.session_state.questions)} (Tech: {question['tech']})")
        st.write(question["question"])

        default_answer = ""
        if idx < len(st.session_state.answers):
            default_answer = st.session_state.answers[idx]["answer"]

        answer = st.text_area("Your answer:", value=default_answer, key=f"answer_{idx}")

        if st.button("Submit Answer", key=f"submit_{idx}"):
            if not answer.strip():
                st.warning("Please enter an answer before submitting.")
                return
            if idx < len(st.session_state.answers):
                st.session_state.answers[idx]["answer"] = answer.strip()
            else:
                st.session_state.answers.append(
                    {"question": question["question"], "answer": answer.strip(), "tech": question["tech"]}
                )
            st.session_state.current_q_index += 1
            st.rerun()

    elif st.session_state.step == "summary":
        ci = st.session_state.candidate_info
        st.header("Candidate Information")
        for key, val in ci.items():
            if key != "tech_stack":
                st.write(f"{key.replace('_',' ').title()}: {val}")
        st.write(f"Tech Stack: {', '.join(ci.get('tech_stack', []))}")

        st.header("Your Answers")
        for i, a in enumerate(st.session_state.answers, 1):
            st.markdown(f"**Q{i} ({a['tech']}):** {a['question']}")
            st.markdown(f"*Answer:* {a['answer']}")

        if st.button("Finish Interview"):
            save_interview_to_excel(ci, st.session_state.answers)
            st.success("Thank you for completing the interview! Data saved.")
            st.session_state.step = "done"
            st.rerun()

    elif st.session_state.step == "done":
        st.write("Interview finished. Goodbye!")
