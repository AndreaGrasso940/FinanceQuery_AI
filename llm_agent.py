import pandas as pd
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate

def analyze_data_with_llm(df, user_question):
    llm = ChatOllama(model="llama3.2", temperature=0)

    # BRAIN 1: THE TRANSLATOR

    code_prompt = """
    You are a strict Data Analyst expert in Python and Pandas.
    You already have a pandas DataFrame loaded in memory named `df`.
    The columns are: {columns}

    The user asks: "{question}"

    Write ONLY the raw Python code to calculate the answer.
    Assign the final calculated value to a variable named `result`.

    CRITICAL RULES:
    1. DO NOT create mock data. Use the existing `df` directly.
    2. DO NOT redefine or recreate the variable `df`.
    3. DO NOT use print(), no markdown, no explanations.
    4. NO YES-MAN POLICY: If the user's request is ambiguous, lacks context, or is impossible to calculate with the given columns, DO NOT guess.
       Instead, assign to the variable `result` a string starting exactly with "CLARIFICATION: " followed by the question you need to ask the user to proceed.
       Example: result = "CLARIFICATION: Do you mean the daily or monthly average?"
    """

    template_code = PromptTemplate.from_template(code_prompt)
    message_code = template_code.format(columns=list(df.columns), question=user_question)

    try:
        # 1. Ask the model ONLY for the code
        response_code = llm.invoke(message_code).content.strip()
        clean_code = response_code.replace('```python', '').replace('```py', '').replace('```', '').strip()

        # 2. Execute the code
        local_environment = {'df': df, 'pd': pd, 'result': None}
        exec(clean_code, local_environment)
        exact_value = local_environment.get('result')

        if exact_value is None:
            return f"The code was executed, but it didn't save anything in the 'result' variable.\n\nGenerated code:\n`{clean_code}`"

        # 2.5: Anti-Yes-Man check (If the model asked for clarification)
        if isinstance(exact_value, str) and exact_value.startswith("CLARIFICATION:"):
            model_doubt = exact_value.replace("CLARIFICATION:", "").strip()
            return f"**I need a clarification:** {model_doubt}"


        # BRAIN 2: THE CONSULTANT

        consultant_prompt = """
        You are an expert financial assistant. The user asked this question: "{question}"

        I have already calculated the exact mathematical result from their real financial data, and it is: {value}

        Answer the user in a conversational and professional way in English.
        MANDATORY RULES:
        1. Start directly by providing the exact result I gave you, without preamble.
        2. Immediately after, offer a single sentence of logical financial advice based ONLY on that number.
        3. DO NOT explain your reasoning, DO NOT cite your instructions, and DO NOT use preambles or greetings.
        """

        template_consultant = PromptTemplate.from_template(consultant_prompt)
        message_consultant = template_consultant.format(question=user_question, value=exact_value)

        # 3. Ask for the discursive response
        final_response = llm.invoke(message_consultant).content.strip()

        complete_response = f"{final_response}\n\n---\n*Transparency - Code:* \n```python\n{clean_code}\n```"

        return complete_response

    except Exception as e:
        error_msg = (
            f"Technical error or incomprehensible question for the model.\n\n"
            f"**Error:** `{str(e)}`\n\n"
            f"**Attempted code:**\n```python\n{clean_code if 'clean_code' in locals() else 'No code generated'}\n```"
        )
        return error_msg
