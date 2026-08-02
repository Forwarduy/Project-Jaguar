![Jaguar Logo](logo.png)

# Project Jaguar 🐆
### The open-source multi-agent platform for solopreneurs.

> Affordable alternative to enterprise AI operations teams. Built for builders who need to move fast.

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

## 🤖 Agents

Project Jaguar includes autonomous agents that work together:

- **Research Agent**: Market research, competitor analysis, trend detection
- **Planning Agent**: OKR generation, project roadmaps, task breakdown
- **Outreach Agent**: Personalized emails, LinkedIn automation
- **Workflow Agent**: n8n integrations, API orchestration

## ✨ Features

- CLI first - run any agent with `python main.py <agent>`
- MCP Server ready - connect to Claude Desktop
- n8n Workflows - 10+ templates included
- 100% Open Source - MIT Licensed

## 🚀 Quick Start

```bash
git clone https://github.com/Forwarduy/Project-Jaguar.git
cd Project-Jaguar
pip install -r requirements.txt
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env
python main.py hello
