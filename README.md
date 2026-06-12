# Assistente Finanziario AI

Un assistente finanziario personale basato su Intelligenza Artificiale locale. Analizza i tuoi bilanci, caricando un semplice foglio Excel, e interagisci con i tuoi dati attraverso una comoda chat, il tutto garantendo la **privacy totale** al 100% (nessun dato viene inviato su server esterni).

## Caratteristiche

- **Privacy First:** L'analisi avviene interamente in locale sul tuo computer.
- **Upload Dinamico:** Carica il tuo foglio Excel (`.xlsx`) e l'AI lo leggerà istantaneamente.
- **Motore LLM Avanzato:** Utilizza il modello Qwen3 4B accoppiato con un agente per eseguire calcoli matematici e interrogazioni dirette sui dati finanziari.
- **Interfaccia:** Chatbot web pulito e reattivo basato su Streamlit.

## Requisiti di Sistema

Per far girare questo progetto, hai bisogno di:

- Python
- Ollama

## Installazione (Linux / Arch Linux)

**1. Clona il repository**

```bash
git clone git@github.com:AndreaGrasso940/fin_ai.git
cd fin_ai
```

**2. Scarica il modello AI locale**

Assicurati che il servizio Ollama sia attivo (`sudo systemctl start ollama` su Arch), poi scarica il modello:

```bash
ollama pull qwen3:4b
```

**3. Crea un ambiente virtuale e installa le dipendenze**

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Come usarlo

1. Avvia l'ambiente virtuale:

```bash
source venv/bin/activate
```

2. Lancia l'interfaccia utente:

```bash
streamlit run main.py
```

3. Il browser si aprirà automaticamente (solitamente su `http://localhost:8501`).
4. **Step 1:** Trascina il tuo file Excel contenente i dati finanziari (colonne suggerite: `Data`, `Tipo`, `Categoria`, `Importo`).
5. **Step 2:** Fai la tua domanda nella chat (es. *"Quali sono i costi che incidono maggiormente?"* o *"Somma tutte le spese per l'Affitto"*).

## Struttura del Progetto

| File | Descrizione |
|---|---|
| `main.py` | Interfaccia utente e gestione del caricamento file con Streamlit. |
| `llm_agent.py` | Logica dell'agente AI che collega LangChain, Pandas e Ollama. |
| `data_generator.py` | Script per generare un file Excel con dati fittizi per i test. |
| `requirements.txt` | Elenco delle dipendenze Python. |
