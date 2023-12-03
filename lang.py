import os
import openai,langchain
from dotenv import load_dotenv
load_dotenv()
 
api_key=os.getenv("OPENAI_KEY",None)

# importing long-chain and initializing an LLM as follows:
from langchain.llms import OpenAI
 
# We are initializing it with a high temperature which means that the results will be random and less accurate. For it to be more accurate you can give a temperature as 0.4 or lesser. 
# We are then assigning openai_api_key as api_key which we have loaded previously from .env file.

llm = OpenAI(temperature=0.9,openai_api_key=api_key)

# The next step would be to predict by passing in the text as follows:
response=llm.predict("Suggest me a skill that is in demand?")
print(response)