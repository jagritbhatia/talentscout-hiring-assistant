from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from chatbot.llm import llm

system_prompt = SystemMessagePromptTemplate(
    prompt=PromptTemplate(
        template="You are an expert technical interviewer.",
        input_variables=[]
    )
)
human_prompt = HumanMessagePromptTemplate(
    prompt=PromptTemplate(
        template="Generate 3 clear, relevant, and challenging technical interview questions about {tech}. "
                 "Return only the questions separated by newlines.",
        input_variables=["tech"]
    )
)

chat_prompt = ChatPromptTemplate.from_messages([system_prompt, human_prompt])

llm_chain = LLMChain(llm=llm, prompt=chat_prompt)

def generate_questions(tech_stack):
    questions = []
    for tech in tech_stack:
        result = llm_chain.invoke({"tech": tech})

        if isinstance(result, dict) and "text" in result:
            output_text = result["text"]
        else:
            output_text = str(result)

        lines = [line.strip("0123456789. ") for line in output_text.split("\n") if line.strip()]
        for q in lines[:3]:
            questions.append({"tech": tech, "question": q})
    return questions
