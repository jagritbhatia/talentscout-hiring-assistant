import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    PromptTemplate,
)
from langchain.chains import LLMChain

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise EnvironmentError("GEMINI_API_KEY must be set in .env")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", google_api_key=GEMINI_API_KEY, temperature=0
)

# Validation prompt chain
validate_system_prompt = SystemMessagePromptTemplate(
    prompt=PromptTemplate(
        template="You are an assistant that checks if a user-provided tech stack is relevant.",
        input_variables=[],
    )
)
validate_human_prompt = HumanMessagePromptTemplate(
    prompt=PromptTemplate(
        template="Is the following tech stack relevant and valid for technical interview purposes? Answer only 'yes' or 'no'.\nTech stack: {tech_stack}",
        input_variables=["tech_stack"],
    )
)
validate_prompt = ChatPromptTemplate.from_messages(
    [validate_system_prompt, validate_human_prompt]
)
validate_chain = LLMChain(llm=llm, prompt=validate_prompt)

# Question generation prompt chain
question_system_prompt = SystemMessagePromptTemplate(
    prompt=PromptTemplate(
        template="You are an expert technical interviewer.", input_variables=[]
    )
)
question_human_prompt = HumanMessagePromptTemplate(
    prompt=PromptTemplate(
        template="Generate 3 clear and relevant technical questions about {tech}.\nList only questions each on a new line.",
        input_variables=["tech"],
    )
)
question_prompt = ChatPromptTemplate.from_messages(
    [question_system_prompt, question_human_prompt]
)
question_chain = LLMChain(llm=llm, prompt=question_prompt)


def is_tech_stack_relevant(tech_stack_text: str) -> bool:
    result = validate_chain.invoke({"tech_stack": tech_stack_text})
    text = result.get("text", "").strip().lower()
    return text == "yes"


def generate_questions(tech_stack_list: list) -> list:
    questions = []
    for tech in tech_stack_list:
        res = question_chain.invoke({"tech": tech})
        text = res.get("text", "")
        lines = [line.strip("0123456789. ") for line in text.split("\n") if line.strip()]
        questions.extend([{"tech": tech, "question": q} for q in lines[:3]])
    return questions
