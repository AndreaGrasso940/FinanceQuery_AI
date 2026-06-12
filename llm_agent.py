from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_ollama import ChatOllama

def analizza_dati_con_llm(df, domanda_utente):
    # Usiamo il modello Qwen3 4B
    llm = ChatOllama(model="qwen3:4b", temperature=0)

    # Creiamo l'agente senza vecchi parametri obsoleti
    agente = create_pandas_dataframe_agent(
        llm,
        df,
        verbose=True,
        allow_dangerous_code=True
    )

    # Istruzione tecnica per evitare l'errore dei backtick nel codice
    istruzione_anti_errore = (
        "\n\nREGOLA TASSATIVA: Nel tuo 'Action Input', scrivi ESCLUSIVAMENTE il codice Python puro. "
        "NON USARE MAI i backtick (```), NON scrivere ```python o ```py. Solo codice eseguibile."
    )

    # Uniamo la tua domanda all'istruzione
    domanda_guidata = domanda_utente + istruzione_anti_errore

    try:
        risposta = agente.invoke(domanda_guidata)
        return risposta["output"]
    except Exception as e:
        return f"Scusa, ho riscontrato un errore tecnico nell'analisi: {str(e)}"
