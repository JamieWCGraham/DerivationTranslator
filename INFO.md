Yes. Here’s a tight **project summary** plus a **Cursor-ready spec** for a lightweight V1 of the **Derivation Translator**.

---

# Project Summary

## Project: Derivation Translator

### Overview

Derivation Translator is a lightweight AI-assisted research tool that helps users understand mathematical steps in technical papers.

The tool takes in a PDF or pasted excerpt from a paper and translates a selected derivation into a clearer, more structured explanation. Rather than summarizing the whole paper, it focuses specifically on the places where readers get stuck: transitions between equations, omitted algebraic steps, hidden assumptions, and missing intuition.

The first version is designed as a simple interactive app for students, researchers, and technically literate readers working through math-heavy papers in physics, applied math, machine learning, or related fields.

### Core User Problem

Many papers contain derivations that look like:

* Equation (7)
* “Therefore...”
* Equation (8)

with little or no explanation of the intermediate reasoning.

Readers often struggle to determine:

* what rule was used
* what substitution occurred
* what assumption was invoked
* whether a step is algebraic, conceptual, or approximate
* what the step means intuitively

The tool aims to reduce this friction by converting dense derivation text into a structured explanatory format.

### Initial Target User

The initial user is a technically capable reader of research papers, such as:

* graduate students
* researchers entering a new subfield
* engineers reading theory-heavy papers
* self-directed learners in physics / math / ML

### V1 Scope

The first version should do only a few things:

1. accept PDF upload or pasted text
2. allow the user to paste or isolate a derivation / equation block
3. send that excerpt to an LLM
4. return structured output with:

   * what happened step by step
   * assumptions used
   * mathematical rules invoked
   * intuitive explanation
   * possible ambiguities / uncertainty

### Why This Project

This is a good first experiment because it is:

* small in scope
* aligned with technical/research interests
* feasible with a lightweight Python stack
* useful even as a local-only prototype
* a strong way to practice structured LLM product design

### Non-Goals for V1

The first version should not try to:

* be a full research assistant
* explain entire papers end-to-end
* build citation graphs
* use a vector database
* support user accounts or history
* guarantee mathematically perfect symbolic proof verification

This is an explainer, not a formal theorem prover.

---

# Cursor Spec

## Derivation Translator — Cursor Build Spec

### Goal

Build a lightweight local-first prototype of an AI-powered derivation explainer using:

* Streamlit
* Python
* OpenAI Responses API
* Pydantic
* PyMuPDF
* python-dotenv

The app should let a user upload a paper PDF or paste text, select or paste a derivation excerpt, and receive a structured explanation of the mathematical transition.

---

## Product Requirements

### Main User Flow

The user should be able to:

1. open the Streamlit app
2. either:

   * upload a PDF, or
   * paste text manually
3. view extracted text from the PDF
4. paste a specific derivation excerpt into a dedicated input box
5. click **Explain Derivation**
6. receive a structured explanation containing:

   * step-by-step explanation
   * assumptions
   * rules / identities used
   * intuition
   * uncertainties / ambiguities

### UX Principles

* Keep the interface minimal
* Bias toward clarity over features
* Make the output easy to scan
* Make uncertainty explicit
* Do not overclaim mathematical correctness

---

## Technical Stack

### Required Libraries

Use:

* `streamlit`
* `openai`
* `pydantic`
* `pymupdf`
* `python-dotenv`

Optional:

* `pandas` only if useful later
* no database for V1

### Environment

Use a `.env` file with:

```bash
OPENAI_API_KEY=your_key_here
```

---

## File Structure

Use this structure:

```text
derivation-translator/
│
├── app.py
├── llm.py
├── parse.py
├── schemas.py
├── prompts.py
├── utils.py
├── requirements.txt
├── .env
└── README.md
```

---

## Functional Requirements

### 1. PDF Parsing

Implement PDF parsing in `parse.py`.

Requirements:

* extract text from uploaded PDF using PyMuPDF
* concatenate pages into a single string
* preserve enough spacing/newlines for readability
* handle parsing failures gracefully

Functions:

* `extract_text_from_pdf(uploaded_file) -> str`

### 2. Structured Output Schema

Implement Pydantic models in `schemas.py`.

Use models similar to:

```python
from typing import Literal, List
from pydantic import BaseModel

class DerivationStep(BaseModel):
    step_number: int
    explanation: str
    rule_or_operation: str | None = None

class DerivationExplanation(BaseModel):
    summary: str
    steps: List[DerivationStep]
    assumptions: List[str]
    intuition: str
    ambiguities: List[str]
    confidence: Literal["low", "medium", "high"]
```

The model should enforce predictable output.

### 3. Prompt Design

Implement prompts in `prompts.py`.

Need:

* one system prompt
* one user prompt template

The system prompt should instruct the model to:

* act as a careful mathematical explainer
* explain derivation transitions conservatively
* distinguish between explicit steps and inferred steps
* state uncertainty when the derivation is ambiguous
* avoid pretending to verify formal correctness if not certain

The user prompt should include:

* the selected derivation text
* optional surrounding context
* explicit instruction to output structured JSON matching schema

### 4. LLM Integration

Implement OpenAI call in `llm.py`.

Requirements:

* call the OpenAI Responses API
* use structured output aligned with the Pydantic schema
* return parsed validated object
* handle API errors gracefully

Function:

* `explain_derivation(derivation_text: str, context_text: str | None = None) -> DerivationExplanation`

### 5. Streamlit App

Implement the UI in `app.py`.

Sections:

* title and short description
* PDF upload
* extracted text preview
* manual text paste option
* derivation input text area
* optional context input area
* explain button
* structured results display

Display output in sections:

* Summary
* Step-by-step explanation
* Assumptions
* Intuition
* Ambiguities
* Confidence

### 6. Error Handling

The app should:

* show a friendly error if no derivation is provided
* show a friendly error if the PDF cannot be parsed
* handle empty model responses
* handle invalid structured output
* avoid crashing on malformed input

---

## Output Behavior

The model output should feel like this:

### Summary

A concise explanation of what the derivation step is doing overall.

### Step-by-step explanation

A numbered list of intermediate mathematical moves.

### Assumptions

Examples:

* linearity
* differentiability
* periodic boundary conditions
* symmetry of operator
* neglecting higher-order terms

### Intuition

Explain the meaning of the move in plain but technically respectful language.

### Ambiguities

Examples:

* “The derivation appears to skip a substitution step.”
* “It is unclear whether the author is assuming small-angle approximation here.”

### Confidence

Low / medium / high depending on how explicit the source derivation is.

---

## Non-Goals

Do not implement in V1:

* authentication
* user accounts
* cloud database
* saved history
* vector search
* multi-paper retrieval
* symbolic algebra engine
* citation graphing
* equation OCR
* formal proof checking

---

## Acceptance Criteria

The app is successful if:

1. a user can upload a PDF and extract text
2. a user can paste a derivation excerpt
3. clicking the button returns structured explanation
4. the output is readable and segmented
5. the app handles common failures gracefully
6. the full app runs locally with minimal setup

---

## Suggested Implementation Order

### Phase 1

* create file structure
* install dependencies
* set up `.env`
* build Pydantic schema

### Phase 2

* implement OpenAI call with mock input
* validate structured output parsing

### Phase 3

* implement PDF extraction

### Phase 4

* build Streamlit UI

### Phase 5

* polish error handling and formatting

---

## README Requirements

The README should include:

* what the project does
* the lightweight stack
* how to install dependencies
* how to add the API key
* how to run the app
* known limitations

---

## Cursor Instruction Block

You can paste this directly into Cursor:

```text
Build a lightweight local-first prototype called Derivation Translator.

Tech stack:
- Python
- Streamlit
- OpenAI Responses API
- Pydantic
- PyMuPDF
- python-dotenv

Goal:
Create a simple app where a user can upload a PDF or paste text, then paste a specific mathematical derivation excerpt and receive a structured explanation.

The app should:
1. accept PDF upload
2. extract text from the PDF
3. allow the user to paste a derivation excerpt into a dedicated text box
4. optionally allow extra surrounding context
5. send the derivation to an LLM
6. return structured output with:
   - summary
   - step-by-step explanation
   - assumptions
   - intuition
   - ambiguities
   - confidence

Use this file structure:
- app.py
- llm.py
- parse.py
- schemas.py
- prompts.py
- utils.py
- requirements.txt
- README.md

Implementation requirements:
- use PyMuPDF for PDF text extraction
- use Pydantic for output schema validation
- use OpenAI Responses API for generation
- use a clean Streamlit UI
- handle errors gracefully
- keep code modular and simple
- no database, auth, vector DB, OCR, or cloud deployment in V1

Pydantic schema should include:
- DerivationStep
- DerivationExplanation

The model should be instructed to explain conservatively, separate explicit vs inferred reasoning, and state uncertainty when necessary.

Return code that is clean, minimal, and runnable locally.
```

---

If you want, I can turn this into an even more actionable package with:

1. a full `README.md`,
2. a starter `requirements.txt`,
3. and the initial prompt/schema code.
