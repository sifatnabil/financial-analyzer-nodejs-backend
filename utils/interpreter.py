from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from dotenv import dotenv_values

def interpret(current_summary, previous_summary):
    config = dotenv_values(".env")
    openai_api_key = config["OPENAI_API_KEY"]

    llm = ChatOpenAI(openai_api_key=openai_api_key, 
                     model_name="gpt-3.5-turbo",
                     temperature=0)
    
    prompt_template = """
    Act as a financial advisor for the user. You have access to user's current financial status and the changes in their financial status.
    Please provide a summary of the user's financial status, including their current spending, earning, and spending percentage, as well as any anomalies detected.
    combine the two objects into a single object and convert it to human-readable text. If information about change in the financial status is missing, 
    provide the summary of the user's financial status without the changes.

    Here is the current summary: {current_summary}

    and here is the change in the financial status: {comparison}

    """

    prompt = PromptTemplate(template=prompt_template, input_variables=["current_summary", "comparison"])

    llm_chain = LLMChain(
        llm=llm,
        prompt=prompt
    )

    answer = llm_chain.predict(current_summary=current_summary, comparison=previous_summary)

    return answer