# Boostify

Bot Discord para registrar mensagens de boost e atribuir um cargo a membros com dois ou mais boosts registrados. Cada instalação atende **um servidor** e mantém seus próprios dados locais.

## Instalação

1. Instale Python 3.13 ou superior e crie um ambiente virtual: `python -m venv .venv`.
2. Ative-o e instale as dependências: `pip install -r requirements.txt`.
3. Copie `.env.example` para `.env` e informe o token do bot. Nunca publique o token.
4. No portal de desenvolvedores do Discord, ative os intents privilegiados **Server Members** e **Message Content**. Convide o bot para o servidor.
5. Dê ao bot acesso ao canal de mensagens de boost, com permissões para visualizar canal, ler histórico e enviar mensagens. Conceda **Gerenciar cargos** e posicione o cargo do bot acima do cargo double booster. O canal e o cargo precisam existir antes da configuração.
6. Execute `python main.py`. No servidor, um administrador ou dono do bot configura:

```text
bb.config canal #canal-de-boosts
bb.config cargo @DoubleBooster
bb.sincronizar
```

Configure o canal em que o Discord publica suas mensagens de boost. `bb.sincronizar` percorre todo o histórico acessível desse canal; em canais grandes pode demorar. A instância fica vinculada ao primeiro servidor configurado. Para usar outro servidor, inicie uma instalação com diretório de dados novo.

## Comandos

Apenas o dono do bot, administradores do servidor e membros com cargo confiável podem usar os comandos administrativos. Somente o dono ou administradores podem conceder e remover confiança.

- `bb.config`: mostra a configuração; `bb.config canal #canal` e `bb.config cargo @cargo` a alteram.
- `bb.confiavel`: lista cargos; `bb.confiavel add @cargo` e `bb.confiavel rm @cargo` gerenciam o acesso.
- `bb.view @membro`: consulta a contagem; sem membro, consulta o autor.
- `bb.setboost @membro 2`: corrige manualmente a contagem e tenta ajustar o cargo.
- `bb.sincronizar`: processa mensagens de boost ainda não registradas no histórico acessível.
- `bb.help`: mostra os comandos.

Os arquivos `data/boosts.json`, `data/admins.json` e `data/config.json` são criados automaticamente e não devem ser publicados. Faça backup dos três juntos, com o bot parado. `DATA_DIR` permite mudar o diretório. Para uma instalação nova em uma cópia que já tenha dados antigos, escolha um `DATA_DIR` vazio; o formato antigo não é migrado nem sobrescrito automaticamente. O arquivo de boosts começa sem registros; IDs de mensagens processadas evitam contagem duplicada entre reinícios e sincronizações.

## Limitações da contagem

O bot conta mensagens de sistema que encontra no canal configurado; elas não são uma fonte garantida da quantidade atual de boosts. Mensagens apagadas, inacessíveis ou publicadas em outro canal não podem ser recuperadas por essa sincronização. Perdas individuais de boosts e mudanças enquanto o bot está desligado podem não ser detectadas. Quando o membro perde o status de booster enquanto o bot está online, a contagem é zerada; processar mensagens antigas pela primeira vez pode voltar a somá-las. Revise a contagem e use `bb.setboost` para corrigir divergências. A leitura do histórico não é uma reconstrução confiável dos boosts ativos nem substitui essa revisão.

Caso a atualização de cargo falhe após salvar a contagem, corrija as permissões e execute `bb.setboost` com o valor atual. Alterar canal ou cargo não migra nem recalcula dados anteriores automaticamente.

## Discloud (opcional)

`discloud.config` é um exemplo genérico e opcional. Consulte a configuração atual da plataforma, forneça `TOKEN` como variável de ambiente e confirme que o armazenamento de `DATA_DIR` persiste entre reinícios e implantações. Sem armazenamento persistente os registros podem ser perdidos. Não inclua `.env` nem dados reais no pacote publicado.

## Desenvolvimento

Instale `pip install -r requirements.txt pytest` e execute `python -m pytest`. O arquivo `requirements.txt` fixa as dependências de execução; `pyproject.toml` registra os metadados e a dependência de testes.

Antes de tornar um repositório existente público, audite todo o histórico Git para dados pessoais e credenciais; arquivos removidos da versão atual ainda podem estar no histórico. Revogue credenciais expostas e remova dados indevidos do histórico antes da publicação.

Licença MIT; consulte `LICENSE`.
