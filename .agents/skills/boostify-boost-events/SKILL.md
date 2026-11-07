---
name: boostify-boost-events
description: Desenvolver ou investigar contagem de boosts, processamento de mensagens, sincronização de histórico e cargos no Boostify.
---

# Eventos e contagem de boosts

Consulte `cogs/eventos.py`, `cogs/gestor.py` e os testes pertinentes. Leia `MEMORY.md` para as decisões de produto.

- Distinga contagem histórica registrada de boosts ativos: mensagens ausentes, perda de boosts e períodos offline podem impedir a reconstrução exata. Não prometa sincronização exata sem verificar os recursos atuais do Discord.
- Considere a filtragem por servidor, canal e tipo de mensagem, a deduplicação por ID persistido e a interação entre eventos em tempo real e `bb.sincronizar`.
- Avalie zeramentos e processamento posterior de mensagens antigas, falhas de permissão ou hierarquia e o registro salvo antes de uma falha ao atualizar o cargo.
- Ao mudar formato de dados ou significado da contagem, avalie compatibilidade, migração e backups; não sobrescreva dados existentes. Mantenha as limitações e os comandos do README atualizados.
- Valide os cenários afetados com dados temporários e mocks quando apropriado. Consulte documentação oficial da API se a solução depender de garantias atuais do Discord.
