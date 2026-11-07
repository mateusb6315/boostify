---
name: boostify-admin-commands
description: Desenvolver ou revisar comandos administrativos, configurações e controle de acesso do bot Discord Boostify.
---

# Comandos administrativos

Consulte `cogs/admin.py`, a persistência usada pelos comandos e os testes pertinentes. Confira `MEMORY.md` para as decisões de produto.

- A instância atende um servidor. O canal de rastreamento e o cargo double booster já existem no Discord e são configurados por comandos.
- O dono do bot, administradores e membros de cargos confiáveis podem usar os comandos administrativos. Apenas dono e administradores alteram a lista de cargos confiáveis. Preserve essa política, salvo pedido do usuário.
- Cargos confiáveis podem alterar configuração e contagem; a seleção de cargos é responsabilidade da administração do servidor. Avalie e documente os efeitos de mudanças de autorização.
- Ao alterar comandos, considere mensagens diretas, vínculo com o servidor, conversão de argumentos e falhas de acesso ou hierarquia no Discord. Valide com dados temporários e mocks quando apropriado.
- Atualize os comandos e as instruções de configuração no README quando a interface mudar.
