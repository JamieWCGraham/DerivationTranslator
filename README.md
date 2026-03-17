# Derivation Translator

A lightweight local-first prototype that explains mathematical derivation steps using an AI model. Upload a paper PDF or paste text, select a derivation excerpt, and get a structured explanation (steps, assumptions, intuition, ambiguities, confidence).

## Stack

- **Streamlit** — UI
- **Python 3.10+**
- **OpenAI API** — explanations (JSON output)
- **Pydantic** — structured output schema
- **PyMuPDF** — PDF text extraction
- **python-dotenv** — environment variables

## Install

```bash
cd DerivationTranslator
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## API key

1. Copy `.env.example` to `.env`.
2. Set your OpenAI API key in `.env`:

   ```bash
   OPENAI_API_KEY=your_key_here
   ```

The app loads `.env` automatically. Do not commit `.env` or share your key.

## Run

From the `DerivationTranslator` directory:

```bash
streamlit run app.py
```

Then open the URL shown in the terminal (usually http://localhost:8501).

## Usage

1. Optionally upload a PDF or paste full text; use the expander to preview extracted/pasted text.
2. Paste the **derivation excerpt** you want explained into the first text area.
3. Optionally add **context** (surrounding sentences) in the second text area.
4. Click **Explain Derivation**.
5. Read the structured result: summary, step-by-step explanation, assumptions, intuition, ambiguities, and confidence.

## Known limitations

- No authentication, user accounts, or saved history.
- No vector search, multi-paper retrieval, or formal proof checking.
- Explanations are best-effort; the app does not verify mathematical correctness.
- PDF extraction may be imperfect for heavily equation or layout-dependent papers.
- Requires an OpenAI API key and network access for the explain step.
