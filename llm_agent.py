from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_ollama import ChatOllama

def analizza_dati_con_llm(df, domanda_utente):
    llm = ChatOllama(model="qwen3:4b", temperature=0)

    agente = create_pandas_dataframe_agent(
        llm,
        df,
        verbose=True,
        allow_dangerous_code=True
    )

    istruzione_anti_errore = (
        "\n\nREGOLA TASSATIVA: Nel tuo 'Action Input', scrivi ESCLUSIVAMENTE il codice Python puro. "
        "NON USARE MAI i backtick (```), NON scrivere ```python o ```py. Solo codice eseguibile."
    )

    domanda_guidata = domanda_utente + istruzione_anti_errore

    try:
        risposta = agente.invoke(domanda_guidata)
        return risposta["output"]
    except Exception as e:
        return f"Scusa, ho riscontrato un errore tecnico nell'analisi: {str(e)}"
