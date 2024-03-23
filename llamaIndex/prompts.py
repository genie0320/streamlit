from llama_index.core.prompts import PromptTemplate


instruction_str = """\
    1. Convert the query to executable Python code using Pandas.
    2. The final line of code should be a Python expression that can be called with the `eval()` function.
    3. The code should represent a solution to the query.
    4. PRINT ONLY THE EXPRESSION.
    5. Do not quote the expression."""

new_prompt = PromptTemplate(
    """\
    You are working with a pandas dataframe in Python.
    The name of the dataframe is `df`.
    This is the result of `print(df.head())`:
    {df_str}

    Follow these instructions:
    {instruction_str}
    Query: {query_str}

    Expression: """
)

context = """Purpose: The primary role of this agent is to assist users by providing accurate 
            information about world population statistics and details about a country. """

# ---------------------------------------

kr_instruction_str = """\
    1. Read the given article carefully and answer according to the context of the text.
    2. If you need additional information to organize the content, please ask questions."""

kr_prompt = PromptTemplate(
    """\
    You are a satirical writer. Read the following and give a witty answer to your answer.:
    {article_str}

    Follow these instructions:
    {kr_instruction_str}
    Query: {query_str}

    Expression: """
)

kr_context = """Purpose: The primary role of this agent is to assist users by providing accurate 
            information about given articles. """