# TalentScout Hiring Assistant Chatbot

## Project Overview
TalentScout Hiring Assistant is an interactive AI-powered chatbot designed to assist in technical hiring interviews. Using Google Gemini's powerful language model through LangChain, the chatbot dynamically generates relevant technical interview questions based on the candidate’s provided tech skills. It collects candidate information, asks tailored questions one at a time, gathers answers, and finally compiles the entire interview summary into an Excel sheet saved locally. This tool streamlines the interview process, making it efficient and personalized.

---

## Installation Instructions

### Prerequisites
- Python 3.8 or higher installed on your machine.
- A Google Gemini API key.

### Step-by-Step Setup

1. **Clone the repository:**


git clone <repository-url>
cd talentscout_hiring_assistant








2. Create a Python virtual environment:


python -m venv .venv
source .venv/bin/activate 
# On Windows use: .venv\Scripts\activate

3. Install dependencies:


pip install -r requirements.txt

4. Add your API key:

Create a `.env` file in the project root with:


GEMINI_API_KEY=your_google_gemini_api_key_here


5. Run the application:


streamlit run app.py





---

## Usage Guide

1. Start the chatbot and click **Start Interview**.
2. Fill in your personal details along with your tech stack (comma-separated).
3. After submission, the bot will validate your tech stack.
- If invalid, it will ask you to provide a valid list of technologies.
4. If valid, the bot generates 3 technical questions for each tech you provided.
5. Answer each question one at a time and submit.
6. After all questions, view the interview summary.
7. On finishing, your complete interview details are appended to a local Excel file `interview_summary.xlsx`.
- Each interview is saved as one row with all answers and candidate info.

---

## Technical Details

- Programming Language: Python 3.8+
- Framework: Streamlit for UI and app flow
- LLM Integration: LangChain framework with Google Gemini API (model: gemini-2.5-flash)
- Data Storage: Persistent Excel file stored locally using `pandas` and `openpyxl`
- Environment Management: `.env` file leveraged for securing API keys



---

## Prompt Design

- Tech Stack Validation Prompt:  
The bot sends the entire user-provided tech stack to the LLM with a prompt that asks if the stack is relevant and valid for interview question generation. The model responds `yes` or `no`.

- Question Generation Prompt:  
For each validated technology, the bot sends a prompt asking the LLM to generate 3 relevant technical interview questions, each on a new line.

This approach leverages AI both for validation and question crafting to ensure adaptability and accuracy.

---

## Challenges & Solutions

- Validating User Input:  
Challenge: How to verify if a user's tech stack entered as free text is valid without a predefined list.  
Solution: Use the LLM itself to validate, by sending a yes/no prompt internally and acting based on response.

- Maintaining Interview State in a Stateless Framework: 
Challenge: Streamlit re-runs scripts from scratch on each interaction.  
Solution: Use `st.session_state` extensively to preserve candidate info, questions, current question index, and answers.




- Storing Interview Data Persistently:  
Challenge: Save each candidate's interview responses sequentially in a local file for later reference.  
Solution: Append candidate details and answers as a single row in an Excel file using `pandas`, ensuring all interviews are collected.

- Streamlit App Flow Control:  
Challenge: Trigger UI updates and page navigation after state changes.  
Solution: Use `st.rerun()` judiciously with step flags for clear and controllable UI transitions.

---


