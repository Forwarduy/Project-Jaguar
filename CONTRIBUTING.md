# Contributing to Project Jaguar 🐆

We welcome contributions from the community! Please read our contributing guidelines before submitting pull requests. This is built in public from Montevideo.

## Quick Start for Devs

```bash
git clone https://github.com/Forwarduy/Project-Jaguar.git
cd Project-Jaguar
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python main.py hello
```

## Antes de abrir un PR

- Corré `pytest -v` y confirmá que todo pasa en verde.
- Si agregás una feature, sumá tests (ver `tests/test_research_agent.py` como ejemplo de mocks, no requieren API key real).
- Usá el [PR template](.github/pull_request_template.md) — se completa solo al abrir el PR.
- Para proponer algo grande, abrí un Issue primero, antes de invertir tiempo en el PR.

## Estilo

Python 3.10+. Sin linter estricto configurado todavía — mantené el estilo del archivo que estés tocando.
