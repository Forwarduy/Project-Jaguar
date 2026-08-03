![Project-Jaguar Logo](logo.png)

# Project-Jaguar

[![CI](https://github.com/Forwarduy/Project-Jaguar/actions/workflows/ci.yml/badge.svg)](https://github.com/Forwarduy/Project-Jaguar/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

AI agent framework for solopreneurs — CLI multi-agente, pensado con arquitectura limpia y CI/CD.

## Estado actual

Solo el **Research Agent** está funcional hoy. `plan` y `outreach` son comandos placeholder — ver [ROADMAP.md](ROADMAP.md).

## Instalación

```bash
pip install -r requirements.txt
cp .env.example .env
# editá .env con tu ANTHROPIC_API_KEY
```

## Uso

```bash
python main.py hello
python main.py research --topic "Uruguay EV market"
python main.py --help
```

Más detalle en [USAGE.md](USAGE.md).

## Contribuir

Ver [CONTRIBUTING.md](CONTRIBUTING.md). Nota: la creación de Issues está desactivada en este repo por ahora (Settings → General → Features → Issues, para habilitarla).

## Licencia

MIT — ver [LICENSE](LICENSE).
