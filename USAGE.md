# Usage Guide - Project Jaguar 🐆

## Instalación

```bash
pip install -r requirements.txt
cp .env.example .env
# editá .env y completá ANTHROPIC_API_KEY
```

## Comandos disponibles

### `hello`
Verifica que la instalación funciona.

```bash
python main.py hello
```

### `research` (funcional)
Corre el Research Agent contra la API real de Claude y devuelve 3 insights sobre el tema.

```bash
python main.py research --topic "Uruguay EV market"
```

Requiere `ANTHROPIC_API_KEY` en `.env`. Sin la key, devuelve un mensaje de error claro en vez de fallar. Hoy usa únicamente el conocimiento del modelo — no hace research en vivo (sin Perplexity ni web todavía, ver ROADMAP).

### `plan` / `outreach` (no implementados)
Existen en el CLI pero hoy solo imprimen "Coming soon" — no ejecutan lógica real todavía.

```bash
python main.py plan --goal "..."      # placeholder
python main.py outreach --campaign "..."  # placeholder
```

## Variables de entorno

| Variable | Requerida | Descripción |
|---|---|---|
| `ANTHROPIC_API_KEY` | Sí, para `research` | Key de la API de Anthropic |
| `ANTHROPIC_MODEL` | No | Override del modelo (default: `claude-sonnet-5`) |
