import pandas as pd
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate

def analizza_dati_con_llm(df, domanda_utente):
    llm = ChatOllama(model="llama3.2", temperature=0)

    # ==========================================
    # CERVELLO 1: IL TRADUTTORE (Testo -> Codice)
    # ==========================================
    prompt_codice = """
    You are a strict Data Analyst expert in Python and Pandas.
    You already have a pandas DataFrame loaded in memory named `df`.
    The columns are: {colonne}

    The user asks: "{domanda}"

    Write ONLY the raw Python code to calculate the answer.
    Assign the final calculated value to a variable named `risultato`.

    CRITICAL RULES:
    1. DO NOT create mock data. Use the existing `df` directly.
    2. DO NOT redefine or recreate the variable `df`.
    3. DO NOT use print(), no markdown, no explanations.
    4. NO YES-MAN POLICY: If the user's request is ambiguous, lacks context, or is impossible to calculate with the given columns, DO NOT guess.
       Instead, assign to the variable `risultato` a string starting exactly with "CHIARIMENTO: " followed by the question you need to ask the user to proceed.
       Example: risultato = "CHIARIMENTO: Intendi la media giornaliera o mensile?"
    """

    template_codice = PromptTemplate.from_template(prompt_codice)
    messaggio_codice = template_codice.format(colonne=list(df.columns), domanda=domanda_utente)

    try:
        # 1. Chiediamo al modello SOLO il codice
        risposta_codice = llm.invoke(messaggio_codice).content.strip()
        codice_pulito = risposta_codice.replace('```python', '').replace('```py', '').replace('```', '').strip()

        # 2. Eseguiamo il codice
        ambiente_locale = {'df': df, 'pd': pd, 'risultato': None}
        exec(codice_pulito, ambiente_locale)
        valore_esatto = ambiente_locale.get('risultato')

        if valore_esatto is None:
            return f"⚠️ Il codice è stato eseguito, ma non ha salvato nulla nella variabile 'risultato'.\n\nCodice generato:\n`{codice_pulito}`"

        # 2.5: Controllo anti-Yes-Man (Se il modello ha chiesto un chiarimento)
        if isinstance(valore_esatto, str) and valore_esatto.startswith("CHIARIMENTO:"):
            dubbio_modello = valore_esatto.replace("CHIARIMENTO:", "").strip()
            return f"🤔 **Ho bisogno di un chiarimento:** {dubbio_modello}"

        # ==========================================
        # CERVELLO 2: IL CONSULENTE (Numeri esatti -> Testo)
        # ==========================================
        prompt_consulente = """
        Sei un assistente finanziario esperto. L'utente ti ha fatto questa domanda: "{domanda}"

        Ho già calcolato il risultato matematico esatto dai suoi dati finanziari reali, ed è: {valore}

        Rispondi all'utente in modo colloquiale e professionale in italiano.
        MANDATORY RULES:
        1. Inizia direttamente fornendo il risultato esatto che ti ho dato, senza preamboli.
        2. Subito dopo, offri una singola frase di consiglio finanziario logico basato SOLO su quel numero.
        3. NON spiegare il tuo ragionamento, NON citare le tue istruzioni ("Se la domanda lo richiede...") e NON fare preamboli o saluti.
        """

        template_consulente = PromptTemplate.from_template(prompt_consulente)
        messaggio_consulente = template_consulente.format(domanda=domanda_utente, valore=valore_esatto)

        # 3. Chiediamo la risposta discorsiva
        risposta_finale = llm.invoke(messaggio_consulente).content.strip()

        risposta_completa = f"{risposta_finale}\n\n---\n*⚙️ Trasparenza - Codice:* \n```python\n{codice_pulito}\n```"
        return risposta_completa

    except Exception as e:
        errore_msg = (
            f"❌ Errore tecnico o domanda incomprensibile per il modello.\n\n"
            f"**Errore:** `{str(e)}`\n\n"
            f"**Codice tentato:**\n```python\n{codice_pulito if 'codice_pulito' in locals() else 'Nessun codice'}\n```"
        )
        return errore_msg
