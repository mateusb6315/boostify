---
name: boostify-release
description: Preparar ou executar commit e push de alterações do Boostify para o remoto destinado ao projeto público.
---

# Fluxo Git do Boostify

Consulte `AGENTS.md` para as regras compartilhadas e examine branch, alterações e destino antes de preparar um commit ou push. Preserve alterações preexistentes e inclua somente o escopo solicitado.

A origem autorizada para o repositório público é a branch local `public`; o destino é a branch `main` do remoto `boostify`. Quando solicitado, o comando é `git push boostify public:main`. A `main` remota não é a branch local `main`.

Não envie para `origin` nem a partir da branch local `main`. Se o pedido indicar qualquer uma dessas opções, interrompa e avise para correção. Não faça push forçado, reescrita de histórico, exclusão de refs ou mudança de visibilidade como efeito automático da skill.

Confira que o commit não inclui configuração privada nem dados reais. O histórico antigo contém IDs Discord; uma busca anterior não garante ausência de segredos. Relate o resultado efetivo do envio e qualquer limitação relevante.
