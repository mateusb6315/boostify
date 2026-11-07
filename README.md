# Boostify

O Boostify é um bot para Discord que registra mensagens de boost e gerencia um cargo para membros com dois ou mais boosts registrados. Cada pessoa executa sua própria instância para um servidor, com configuração por comandos e dados armazenados em arquivos JSON locais.

O projeto acompanha as mensagens de sistema do Discord em um canal configurado, mantém uma contagem por membro e tenta adicionar ou remover o cargo escolhido conforme essa contagem. Também oferece comandos para consultar e corrigir registros e processar mensagens disponíveis no histórico do canal.

## Por que o Boostify?

Reconhecer quem apoia uma comunidade ajuda a valorizar sua participação. O Discord oferece um cargo de booster, mas não uma opção nativa de cargo específico para quem concede dois boosts ao mesmo servidor. O Boostify nasceu para preencher essa lacuna e facilitar o reconhecimento desses membros.

Quer oferecer um benefício especial aos double boosters da sua comunidade? Configure um cargo no seu servidor e use o Boostify para acompanhar os registros e gerenciá-lo.

## Requisitos e dependências

- Python 3.13 ou superior e `pip`.
- Uma aplicação e um bot criados no [Discord Developer Portal](https://discord.com/developers/applications), com token disponível e bot convidado para o servidor.
- Um canal configurado no servidor para receber as mensagens de sistema de boost e um cargo double booster já criado.
- Os intents privilegiados **Server Members** e **Message Content** habilitados no portal do Discord.
- Permissões para o bot visualizar o canal, ler seu histórico e enviar mensagens, além de **Gerenciar cargos**. O cargo do bot deve estar acima do cargo double booster na hierarquia do servidor.
- As bibliotecas `discord.py==2.6.4` e `python-dotenv==1.2.1`, instaladas pelo `requirements.txt`.

Para executar os testes de desenvolvimento, instale também `pytest`.

## Quick start

1. Clone a branch `public` e entre no diretório:

   ```bash
   git clone -b public https://github.com/mateusb6315/boostify.git
   cd boostify
   ```

2. Crie e ative um ambiente virtual:

   ```bash
   python -m venv .venv
   ```

   No Windows PowerShell:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   No Linux ou macOS:

   ```bash
   source .venv/bin/activate
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Copie `.env.example` para `.env` e preencha `TOKEN` com o token do bot. Opcionalmente, altere `PREFIX` e `DATA_DIR`, que usam `bb.` e `data` por padrão. Mantenha o token privado.

5. Ative os intents e configure as permissões descritas nos requisitos. Inicie o bot a partir do diretório do projeto:

   ```bash
   python main.py
   ```

6. No servidor, como administrador ou dono do bot, configure o canal e o cargo existentes. Depois, processe as mensagens disponíveis no histórico:

   ```text
   bb.config canal #canal-de-boosts
   bb.config cargo @DoubleBooster
   bb.sincronizar
   ```

O canal deve ser aquele em que o Discord publica as mensagens de boost. A primeira configuração de canal ou cargo vincula a instância ao servidor. Para usar outro servidor, utilize uma instalação com diretório de dados novo.

## Estrutura e funcionamento

```text
boostify/
├── main.py              # Inicialização, intents e carregamento dos módulos
├── cogs/
│   ├── admin.py         # Comandos e verificação de acesso
│   ├── eventos.py       # Mensagens de boost e atualização de cargos
│   └── gestor.py        # Leitura e gravação dos dados
├── config/vars.py       # Variáveis de ambiente e diretório de dados
├── data/                # Criado em execução; não versionado
├── tests/               # Testes automatizados
├── .env.example         # Exemplo de configuração local
├── requirements.txt     # Dependências de execução
├── pyproject.toml       # Metadados e configuração de desenvolvimento
└── discloud.config      # Exemplo opcional para Discloud
```

Na inicialização, o bot lê as variáveis de ambiente, carrega os módulos e cria os arquivos de dados que ainda não existem. Um administrador configura o canal e o cargo. A partir daí, o fluxo é:

1. Uma mensagem de sistema de boost chega ao canal configurado ou é encontrada por `bb.sincronizar` no histórico acessível.
2. O bot verifica o servidor, o canal e o tipo da mensagem. Se o ID da mensagem ainda não foi processado, ele registra o ID e incrementa a contagem do membro.
3. Com dois ou mais boosts registrados, o bot tenta adicionar o cargo configurado. Uma contagem menor que dois leva à tentativa de removê-lo quando o cargo é sincronizado.
4. Se o bot observar que um membro perdeu o cargo nativo de booster, ele zera a contagem desse membro e tenta remover o cargo double booster.

Os IDs das mensagens já processadas são preservados para evitar contagem duplicada em reinícios e sincronizações. O histórico pode ser extenso, portanto `bb.sincronizar` pode demorar.

### Comandos

O prefixo padrão é `bb.`. O dono do bot, administradores do servidor e membros de cargos confiáveis podem usar os comandos administrativos. Somente o dono do bot e administradores podem adicionar ou remover cargos confiáveis.

| Comando | Ação |
| --- | --- |
| `bb.config` | Mostra o canal e o cargo configurados. |
| `bb.config canal #canal` | Define o canal de rastreamento. |
| `bb.config cargo @cargo` | Define o cargo double booster. |
| `bb.confiavel` | Lista os cargos confiáveis. |
| `bb.confiavel add @cargo` | Adiciona um cargo confiável. |
| `bb.confiavel rm @cargo` | Remove um cargo confiável. |
| `bb.view [@membro]` | Consulta a contagem do membro informado ou do autor. |
| `bb.setboost @membro quantidade` | Define a contagem e tenta ajustar o cargo. |
| `bb.sincronizar` | Processa mensagens ainda não registradas no histórico acessível. |
| `bb.help` | Exibe a ajuda dos comandos. |

## Problemas conhecidos e colaboração

Os pontos abaixo são limitações conhecidas e candidatos a melhorias ou correções futuras:

- **Contagem divergente:** as mensagens de sistema não garantem uma visão exata dos boosts ativos. Mensagens apagadas, inacessíveis ou publicadas em outro canal não são recuperadas. Perdas individuais de boosts e mudanças enquanto o bot está desligado podem passar despercebidas.
- **Histórico antigo:** ao processar pela primeira vez mensagens antigas após uma contagem ter sido zerada, elas podem voltar a incrementar o registro. Revise os resultados e use `bb.setboost` para corrigir divergências.
- **Falha ao atualizar o cargo:** a contagem pode ser salva mesmo quando o Discord recusa a alteração do cargo. Verifique as permissões e a hierarquia e execute `bb.setboost` com o valor atual para tentar novamente.
- **Mudanças de configuração:** alterar o canal ou o cargo não migra nem recalcula automaticamente os dados anteriores.
- **Cobertura de testes limitada:** os testes atuais cobrem parte da persistência e do processamento de mensagens; outros fluxos ainda precisam de cobertura.

Encontrou um problema ou tem uma ideia para melhorar o Boostify? Contribuições são bem-vindas! Abra uma issue descrevendo o comportamento e, quando possível, os passos para reproduzi-lo. Você também pode propor uma correção ou melhoria por pull request. Evite incluir tokens ou dados pessoais nos relatos.

Para preparar o ambiente de desenvolvimento e executar os testes:

```bash
pip install -r requirements.txt pytest
python -m pytest
```

## Informações importantes

- **Dados e backups:** `data/boosts.json` armazena contagens e IDs de mensagens, `data/admins.json` guarda os IDs dos cargos confiáveis e `data/config.json` contém a configuração do servidor. Os arquivos são criados automaticamente e começam sem registros; faça backup dos três juntos com o bot parado. Eles não devem ser publicados.
- **Instalações anteriores:** o formato antigo de `boosts.json` não é migrado automaticamente. Para começar uma instalação nova, configure um `DATA_DIR` vazio; o bot não sobrescreve automaticamente um arquivo antigo.
- **Acesso administrativo:** cargos confiáveis podem executar comandos administrativos, inclusive alterar a configuração do cargo e a contagem de membros. Conceda essa confiança com cuidado e considere as permissões dos cargos que o bot pode gerenciar.
- **Segredos:** mantenha `.env` e o token fora do repositório. Se um token for exposto, substitua-o no portal do Discord.
- **Discloud:** `discloud.config` é um template padrão de configuração e opcional para uso no serviço de hospedagem Discloud. Para usá-lo, confira a configuração atual da plataforma, forneça `TOKEN` como variável de ambiente e confirme que `DATA_DIR` possui armazenamento persistente entre reinícios e implantações.

## Licença

O Boostify é distribuído sob a [licença MIT](LICENSE). Ela permite usar, copiar, modificar e distribuir o código, inclusive em projetos comerciais, desde que o aviso de direitos autorais e a licença sejam mantidos. O software é fornecido sem garantias. Consulte o arquivo `LICENSE` para o texto completo.
