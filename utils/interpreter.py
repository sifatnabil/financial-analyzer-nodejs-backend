import asyncio
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from dotenv import dotenv_values

async def interpret(current_summary, previous_summary, prompt):
    config = dotenv_values(".env")
    openai_api_key = config["OPENAI_API_KEY"]

    llm = ChatOpenAI(openai_api_key=openai_api_key, 
                     model_name="gpt-3.5-turbo",
                     temperature=0)
    
    prompt_template = prompt

    prompt = PromptTemplate(template=prompt_template, input_variables=["current_summary", "comparison"])

    llm_chain = LLMChain(
        llm=llm,
        prompt=prompt
    )

    answer = await llm_chain.apredict(current_summary=current_summary, comparison=previous_summary)


    return answer