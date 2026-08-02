![Jaguar Logo](logo.png)

# Project Jaguar 🐆
### The open-source multi-agent platform for solopreneurs

[![CI](https://github.com/Forwarduy/Project-Jaguar/actions/workflows/ci.yml/badge.svg)](https://github.com/Forwarduy/Project-Jaguar/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

**Open-source multi-agent AI platform for strategic planning & business automation. Built in public from Montevideo, UY 🇺🇾**

> Affordable alternative to enterprise AI ops teams. Stop paying $200/mo for basic automation.

---

## 🤖 Agents

| Agent | What it does |
|-------|--------------|
| **Research Agent** | Market research, competitor analysis, trend detection |
| **Planning Agent** | OKR generation, roadmaps, task breakdown |
| **Outreach Agent** | Personalized cold emails, LinkedIn automation |
| **Workflow Agent** | n8n integrations, API orchestration |

## ✨ Features

- **CLI First** - Run any agent with `python main.py <agent>`
- **MCP Server Ready** - Connect to Claude Desktop
- **n8n Workflows** - 10+ templates included in `/workflows`
- **100% Open Source** - MIT Licensed, community-driven

## 🚀 Quick Start

```bash
git clone https://github.com/Forwarduy/Project-Jaguar.git
cd Project-Jaguar
pip install -r requirements.txt
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env
python main.py hello
python main.py --help
