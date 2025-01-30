from kobai import llm_config
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatDatabricks
from langchain.globals import set_debug
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from langchain_openai import AzureChatOpenAI

MESSAGE_SYSTEM_TEMPLATE = """
    You are a data analyst tasked with answering questions based on a provided data set. Please answer the questions based on the provided context below. Make sure not to make any changes to the context, if possible, when preparing answers to provide accurate responses. If the answer cannot be found in context, just politely say that you do not know, do not try to make up an answer.
    When you receive a question from the user, answer only that one question in a concise manner. Do not elaborate with other questions.
    """

MESSAGE_AI_TEMPLATE = """
    The table information is as follows:
    {table_data}
    """

MESSAGE_USER_CONTEXT_TEMPLATE = """
    The context being provided is from a table named: {table_name}
    """

MESSAGE_USER_QUESTION_TEMPLATE = """
    {question}
    """

SIMPLE_PROMPT_TEMPLATE = f"""
    {MESSAGE_SYSTEM_TEMPLATE}

    {MESSAGE_USER_CONTEXT_TEMPLATE}

    {MESSAGE_AI_TEMPLATE}

    Question: {MESSAGE_USER_QUESTION_TEMPLATE}
    """
 
def followup_question(question, data, question_name, llm_config:llm_config, override_model=None):
    
    """
    Use LLM to answer question in the context of provided data.

    Parameters:
    question (str): A natural language question to apply.
    data (str): Simple dictionary-like structured data.
    question_name (str): Dataset name for context.
    llm_config (LLMConfig): User set LLM configurations and some default ones.
    override_model (LangChain BaseLanguageModel) OPTIONAL: Langchain LLM or ChatModel runnable.
    """
    
    set_debug(llm_config.debug)
    
    # If override model is provided, then use the override model as chat model.
    if override_model is not None:
        chat_model=override_model
    elif llm_config.llm_provider == "databricks":
        chat_model = ChatDatabricks(
            endpoint = llm_config.endpoint,
            temperature = llm_config.temperature,
            max_tokens = llm_config.max_tokens,
            )
    elif llm_config.llm_provider == "azure_openai":
        if(llm_config.api_key is None):
            # Authenticate through AZ Login or through service principal
            # Instantiate the AzureChatOpenAI model
            chat_model = AzureChatOpenAI(
                azure_endpoint=llm_config.endpoint,
                azure_deployment=llm_config.deployment,
                azure_ad_token=llm_config.aad_token,
                openai_api_version=llm_config.api_version,
                temperature = llm_config.temperature,
                max_tokens = llm_config.max_tokens,
            ) 
        else:
            # Authenticate through API Key
            chat_model = AzureChatOpenAI(
                api_key = llm_config.api_key,
                azure_endpoint=llm_config.endpoint,
                azure_deployment=llm_config.deployment,
                openai_api_version=llm_config.api_version,
                temperature = llm_config.temperature,
                max_tokens = llm_config.max_tokens,
            )   
    else:
        chat_model = ChatDatabricks(
            endpoint = llm_config.endpoint,
            temperature = llm_config.temperature,
            max_tokens = llm_config.max_tokens,
            )        

    if llm_config.use_simple_prompt: 
        prompt = PromptTemplate.from_template(SIMPLE_PROMPT_TEMPLATE)
    else:
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(MESSAGE_SYSTEM_TEMPLATE),
                HumanMessagePromptTemplate.from_template(MESSAGE_USER_CONTEXT_TEMPLATE),
                AIMessagePromptTemplate.from_template(MESSAGE_AI_TEMPLATE),
                HumanMessagePromptTemplate.from_template(MESSAGE_USER_QUESTION_TEMPLATE)
            ]
        )

    output_parser = StrOutputParser()

    chain = prompt | chat_model | output_parser

    response = chain.invoke(
        {
            "table_name": question_name,
            "table_data": str(data),
            "question": question
        }
    )

    return response