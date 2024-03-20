# pip install llama-index pandas python-dotenv myPDF

from dotenv import load_dotenv
import os
import pandas as pd
from llama_index.core.query_engine import PandasQueryEngine
from prompts import new_prompt, instruction_str, context, kr_prompt, kr_instruction_str, kr_context_str
from note_engine import note_engine
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.readers.file import PDFReader
from llama_index.llms.openai import OpenAI
from llama_index.core.agent import ReActAgent

load_dotenv()

# 세계인구에 대한 케글의 csv
world_path = os.path.join('data', 'world_population.csv')
world_df = pd.read_csv(world_path)

# 한국의 인구절벽에 대한 나무위키의 글
korean_path = os.path.join('data', 'korean_population.pdf')
_korean_pdf = SimpleDirectoryReader(input_files=[korean_path]).load_data()

# 쿼리엔진을 생성해주고
# pandas 의 기능을 이용하기 위한 pandas query engine을 사용.
world_engine = PandasQueryEngine(df=world_df, verbose=True, instruction_str=instruction_str)

# 이쪽은 pdf 문서를 읽어들이므로, pdf리더로 읽어들여 쿼리엔진으로 만듬.
korean_pdf = VectorStoreIndex.from_documents(_korean_pdf)
korean_engine = korean_pdf.as_query_engine(verbose=True, instruction_str=kr_instruction_str)


# 그 엔진에 프롬프트를 주입한다.
world_engine.update_prompts({'pandas_prompt' : new_prompt})
korean_engine.update_prompts({'pandas_prompt' : kr_prompt})

# 쿼리엔진에 질문을 넣는다.
response = korean_engine.query("한국의 출산율이 떨어지는 이유는?")
print(response)


# Agent 가 사용할 수 있는 툴을 제작
tools = [
    note_engine,
    QueryEngineTool(
        query_engine=world_engine,
        metadata = ToolMetadata(
        name="population_data",
        description="this gives information at the world population and demographics",
        )
    ),
    QueryEngineTool(
        query_engine=korean_engine,
        metadata = ToolMetadata(
        name="article about Korea's fertility rate",
        description="a collection of korean writings on Korea's fertility rate from various perspectives",
        )
    ),
]

llm = OpenAI(temperature=0, model="gpt-3.5-turbo")
agent = ReActAgent.from_tools(tools, llm=llm, verbose=True, context=context)

while (prompt := input("Enter a prompt (q to quit): ")) != "q":
    result = agent.query(prompt)
    print(result)