# Project Jaguar Roadmap 🗺️

## Visión
La plataforma multi-agente más accesible para solopreneurs. Alternativa a herramientas enterprise de $200/mes.

## Fase 1 — Fundación
- [x] CLI con Typer + Rich
- [x] BaseAgent abstract class
- [x] CI/CD con GitHub Actions (tests mockeados — no requieren API key real)
- [x] .env setup para Anthropic
- [x] Research Agent (Claude, sin research en vivo todavía)
- [ ] Research Agent con datos reales (Perplexity API u otra fuente para market research / competitor scraping)
- [ ] 3 n8n workflow templates

## Fase 2 — Agentes V1
- [ ] Planning Agent: generación de OKRs, roadmap builder
- [ ] Outreach Agent: cold email con personalización
- [ ] MCP Server para Claude Desktop
- [ ] 10+ n8n workflows

## Fase 3 — Plataforma
- [ ] Web UI (FastAPI + HTMX)
- [ ] Agent marketplace
- [ ] Integraciones: Notion, Slack, Gmail
- [ ] Cloud hosting option
- [ ] Aplicar a los programas de startups de Anthropic y OpenAI

## ¿Querés proponer una feature?
Por ahora la creación de Issues está desactivada en este repo — escribime directamente. (Para habilitarla: Settings → General → Features → tildar Issues.)
