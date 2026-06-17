# FinanceQuery_AI — Local AI Financial Analyst

> **Disclaimer:** This project is a Proof of Concept created for portfolio and technology testing purposes. The system is currently functional and can be used to query private tabular files, but it may contain bugs, unhandled edge cases, or undergo significant refactoring in future versions.
> **It does not provide financial advice of any kind and is not a substitute for the opinion of a qualified professional. The author disclaims all responsibility for economic decisions based on the tool's output.**

---

## Demo

<img width="792" height="938" alt="image" src="https://github.com/user-attachments/assets/912842c2-169a-4662-9618-eed2f2e31844" />


---

## Motivation

**Developed for educational and personal research purposes**, this prototype aims to test the effectiveness of Open Weights LLM models running locally on structured tabular data.

The goal was to build an assistant capable of querying data while guaranteeing absolute privacy. The core objective of this project is to **test these tools in the field**, deeply understand their internal mechanisms (and their limitations), in order to build increasingly solid and advanced architectures in the future.

## "Two Brains" Architecture

FinanceQuery_AI adopts a **deterministic three-phase architecture**:

```
[User question]
       │
       ▼
 ┌─────────────┐
 │   Brain 1   │  ← AI (Llama3.2 via Ollama)
 │  Translator │     Converts the question into pure Python/Pandas code
 └──────┬──────┘
        │
        ▼
 ┌─────────────┐
 │   Python    │  ← Local computation engine
 │   Engine    │     Executes the code on real data → exact result
 └──────┬──────┘
        │
        ▼
 ┌─────────────┐
 │   Brain 2   │  ← AI (Llama3.2 via Ollama)
 │  Consultant │     Formulates a conversational response based on the result
 └─────────────┘
```

**Advantages over classic agents:**
- **Zero mathematical hallucinations** — computation is delegated to Python, not to the AI.
- **Reduced latency** — no repetitive Thought/Action/Observation loops.
- **Anti Yes-Man Policy** — if the question is ambiguous or data is missing, the system asks for clarification instead of making up a plausible answer.

---

## Key Features

- **100% local and privacy-first** — no data sent to external servers or APIs, ideal for sensitive personal and business finances.
- **Dynamic upload** — supports `.xlsx` and `.csv` files; the AI adapts queries to automatically detected columns.
- **Deterministic architecture** — designed to be reliable and predictable, not dependent on emergent model behavior.

---

## Tech Stack

| Component | Technology | Role |
|-----------|------------|------|
| Local LLM | Ollama + Llama3.2 | Natural language → code translation and response generation |
| Data engine | Pandas | Computation execution on real data |
| UI | Streamlit | User interface and file upload |
| Runtime | Python 3.9+ | Architecture orchestration |

---

## Installation

### Linux / Arch Linux

```bash
# 1. Clone the repository
git clone git@github.com:AndreaGrasso940/FinanceQuery_AI.git
cd FinanceQuery_AI

# 2. Start Ollama and download the model
sudo systemctl start ollama
ollama pull Llama3.2

# 3. Create the virtual environment and install dependencies
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Windows (Native)

- Install **Python 3.9+** from [python.org](https://www.python.org/downloads/) — check **"Add Python to PATH"**.
- Install **Git** from [git-scm.com](https://git-scm.com/download/win).
- Install **Ollama** from [ollama.com](https://ollama.com/download/windows) — it starts automatically in the background.

```powershell
# Clone the repository
git clone git@github.com:AndreaGrasso940/FinanceQuery_AI.git
cd FinanceQuery_AI

# Download the model
ollama pull Llama3.2

# Create the virtual environment and install dependencies
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## How to Use

1. Activate the virtual environment:
   - Linux: `source venv/bin/activate`
   - Windows: `venv\Scripts\activate`

2. Launch the interface:
```bash
   streamlit run main.py
```

3. The browser will open at `http://localhost:8501`.

4. **Step 1:** Upload your Excel or CSV file with financial data (suggested columns: `Date`, `Type`, `Category`, `Amount_EUR`).

5. **Step 2:** Ask your question in the chat — e.g. *"Which spending categories have the highest impact?"* or *"Sum all expenses for March"*.

---

## Project Structure

| File | Description |
|------|-------------|
| `main.py` | User interface and upload management with Streamlit. |
| `llm_agent.py` | "Two Brains" architecture logic, code execution, and error handling. |
| `data_generator.py` | Fake data generator for testing. |
| `requirements.txt` | Python dependencies. |

---

## Roadmap / Next Steps

- [ ] Conversational memory (Chat History).
- [ ] Interactive chart generation (Data Visualization).
- [ ] Transition to a Multi-Agent architecture (LangGraph / Autogen) for complex tasks.

---

## License

This project is distributed under the **MIT License**.

```
MIT License

Copyright (c) 2025 Andrea Grasso

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
