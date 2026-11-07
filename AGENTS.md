# Orientações para agentes no Boostify

Leia [MEMORY.md](MEMORY.md) para conhecer o contexto e as decisões duradouras. Confira a implementação e o estado do Git antes de trabalhar: a memória pode estar desatualizada.

## Trabalho no repositório

- Responda em português, salvo solicitação diferente. Preserve alterações existentes e limite o trabalho ao pedido.
- A branch de desenvolvimento para o repositório público é a `public` local. O remoto autorizado para esse repositório é `boostify`, com destino `main`: quando o usuário solicitar o envio, use `git push boostify public:main` após conferir branch, commit e destino.
- Não envie para `origin` nem faça push a partir da branch local `main`. Se o pedido indicar qualquer uma dessas opções, interrompa e avise para correção. A `main` remota de `boostify` é o destino permitido para a `public` local.
- Não altere a visibilidade do repositório nem faça commit ou push sem uma solicitação aplicável do usuário.
- Não inclua tokens, `.env` ou dados reais de `data/` em arquivos versionados, exemplos, testes ou logs.

## Desenvolvimento

- Uma instância atende um servidor; preserve essa premissa salvo pedido explícito para alterá-la.
- Use as skills específicas em `.agents/skills/` quando forem relevantes à tarefa. Elas complementam estas orientações.
- Execute verificações proporcionais à alteração. Para a suíte existente, use `python -m pytest`; não execute o bot contra um servidor real sem autorização adequada.
- Ao alterar comportamento, configuração, comandos ou limitações, mantenha o README coerente. Atualize MEMORY.md quando uma decisão duradoura mudar, evitando segredos e detalhes passageiros.
