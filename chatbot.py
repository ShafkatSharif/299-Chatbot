from langchain_community.llms import ollama
from langchain.chains import retrieval_qa
from langchain.prompts import PromptTemplate

MODEL = "mistral:7b"
llm= ollama(model=MODEL)

template = """
Answer the question based on only physics content which are given. If you can't 
answer the question, reply "I don't know".

Context: {context}

Question: {question}
"""

prompt = PromptTemplate.from_template(template)
prompt.format(context="Here is some context", question="Here is a question")




def get_response(question):
    response = llm.invoke(question)
    return response

print("Welcome to Physics Chatbot!")

while True:
    text = input("Ki jante chas? : ")
    if text in ["exit", "quit"]:
         print("Hedar pola tumi!")
         break
    answer = get_response(text)
    print(answer)
