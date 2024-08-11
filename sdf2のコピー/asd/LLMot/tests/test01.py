import os
from langchain.llms import LlamaCpp
from transformers import pipeline
from langchain.utilities import GoogleSearchAPIWrapper
from langchain.agents import Tool, initialize_agent

file_path = os.path.abspath("modelf/japanese_gpt_neox_3.6b_instruction_ppo.bin")

llm = LlamaCpp(
    model_path=file_path,
    n_ctx=2048,
    temperature=0,
    max_tokens=64,
    verbose=True,
    streaming=True
)

ej_translator = pipeline("translation", model="staka/fugumt-en-ja")
je_translator = pipeline("translation", model="staka/fugumt-ja-en")

search = GoogleSearchAPIWrapper()

tools = [
    Tool(
        name = "Search",
        func=search.run,
        description="A search engine. Useful for when you need to answer questions")
]

ja_text = "日本国内で2番目に標高が高い山は?"
en_text=je_translator(ja_text)[0]['translation_text']
print(en_text)

agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)
output = agent.run(en_text)
output = output.split('\n')[0]

ej_translator(output)[0]['translation_text']