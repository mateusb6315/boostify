# Memória do projeto Boostify

Este arquivo reúne contexto e decisões úteis para continuar o desenvolvimento. Confira o código e a conversa atual antes de agir; atualize esta memória quando decisões duradouras mudarem. Não registre segredos, IDs de usuários ou dados privados aqui.

## Objetivo e funcionamento

- Bot Discord em Python para registrar mensagens de boost e gerenciar um cargo para membros com dois ou mais boosts registrados. Cada pessoa executa sua própria instância para um servidor.
- Canal de rastreamento e cargo double booster já devem existir no servidor e são definidos por comandos. A primeira configuração vincula os dados ao servidor.
- O proprietário do bot, administradores e membros de cargos confiáveis usam comandos administrativos; somente proprietário e administradores podem adicionar ou remover cargos confiáveis. A seleção dos cargos é responsabilidade da administração do servidor.
- As contagens são históricas e baseadas nas mensagens de sistema disponíveis, não uma fonte garantida da quantidade de boosts ativos. O ID da mensagem evita duplicações; `bb.sincronizar` percorre o histórico acessível, e `bb.setboost` permite correção manual.

## Organização e dados

- `main.py` inicializa o bot e carrega `cogs/gestor.py`, `cogs/admin.py` e `cogs/eventos.py`; `config/vars.py` carrega as variáveis de ambiente. Consulte o README para instalação, comandos e permissões.
- `data/boosts.json` guarda contagens e IDs de mensagens processadas; `data/config.json` guarda servidor, canal e cargo; `data/admins.json` guarda cargos confiáveis. Os arquivos são criados quando ausentes e ficam fora do Git. O formato antigo de boosts não é migrado automaticamente.
- `TOKEN` é obrigatório; `PREFIX` e `DATA_DIR` são opcionais. Nunca inclua valores reais de token ou dados locais em documentação ou histórico versionado.
- `cogs/utils.py` é código interno obsoleto, ignorado pelo Git e não carregado pelo bot; não o reincorpore sem solicitação.

## Limitações conhecidas

- Mensagens ausentes, boosts encerrados e eventos durante indisponibilidade podem gerar divergências; histórico antigo pode ser contado após um zeramento. Confira as limitações no README antes de propor uma sincronização exata.
- Uma falha ao atualizar cargo pode ocorrer após salvar a contagem. Alterar canal ou cargo não recalcula os dados anteriores automaticamente.
- O histórico Git contém IDs antigos de Discord; uma busca anterior por padrões comuns não encontrou credenciais, mas não garante sua ausência. O usuário decidiu prosseguir com os riscos identificados; não descreva o histórico como auditado de forma conclusiva.

## Git e distribuição

- `boostify` é o remoto destinado ao projeto público; o repositório estava privado na última informação fornecida pelo usuário. Não presuma que isso mudou.
- Alterações para o repositório público saem da branch local `public` para a branch remota `main`: `git push boostify public:main`, quando solicitado. Não envie para `origin` ou da branch local `main`; alerte o usuário se ele solicitar esses destinos por engano.
- `discloud.config` é genérico e opcional. A persistência do diretório de dados deve ser confirmada na hospedagem.
