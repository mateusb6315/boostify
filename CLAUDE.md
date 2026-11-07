# Boostify — orientações para Claude Code

Leia [MEMORY.md](MEMORY.md) para conhecer o objetivo, a arquitetura e as decisões duradouras. Consulte o código atual antes de assumir que a memória ainda descreve o comportamento. As regras compartilhadas do projeto estão em [AGENTS.md](AGENTS.md).

## Regras de trabalho

- Leia a skill pertinente em `.agents/skills/` para tarefas de eventos de boost, comandos administrativos ou envio ao repositório; ela pode ser consultada diretamente como arquivo Markdown.
- Siga a regra de Git em `AGENTS.md`: a branch local `public` é enviada para `boostify/main` quando solicitado. Não confunda essa `main` remota com a branch local `main`.
- Preserve alterações preexistentes, mantenha o README coerente com mudanças de comportamento e use `python -m pytest` quando apropriado. Atualize `MEMORY.md` apenas para decisões duradouras, sem dados privados.
