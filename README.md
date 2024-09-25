
# Bot de Jogo de Cartas do Discord

Bem-vindo ao **Bot de Jogo de Cartas do Discord**! Este bot permite que os usuários joguem um jogo de cartas onde podem adicionar cartas à sua coleção.

## 📦 Funcionalidades

- **Adicionar Cartas**: Os usuários podem adicionar novas cartas à sua coleção.
- **Coletar Cartas**: Os usuários podem coletar cartas e construir seu próprio deck único.

## 🛠️ Requisitos

Antes de começar, certifique-se de ter o seguinte:

- Python 3.8 ou superior
- Biblioteca Discord.py (Instale usando `pip install discord.py`)
- Um Token de Bot do Discord

## 🔧 Configuração

1. **Clone o Repositório**:

   ```bash
   git clone 
   cd discord-card-game-bot
   ```

2. **Instale as Dependências**:

   Certifique-se de ter os pacotes necessários instalados:

   ```bash
   pip install -r requirements.txt
   ```

3. **Crie um Arquivo `.env`**:

   No diretório raiz do seu projeto, crie um arquivo chamado `.env` e adicione seu token de bot do Discord:

   ```plaintext
   TOKEN=seu_token_do_bot_discord
   ```

   Substitua `seu_token_do_bot_discord` pelo seu token real do bot do Discord.

## 🕹️ Como Executar o Bot

Para iniciar o bot, execute o seguinte comando:

```bash
python Main.py
```

Certifique-se de que seu arquivo `.env` esteja configurado com o token do seu bot para que funcione corretamente.

## 📜 Comandos

- `/add_collection`: Adiciona uma nova coleção.
- `/add_card`: Adiciona uma nova carta à sua coleção.
- `/collect `: Coleta uma carta aleatoria.

## 🤝 Contribuições

Contribuições são bem-vindas! Se você tiver sugestões para melhorias ou novos recursos, por favor, abra uma issue ou envie uma solicitação de pull.

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - consulte o arquivo [LICENSE](LICENSE) para mais detalhes.

---

Sinta-se à vontade para modificar qualquer seção para melhor se adequar ao seu projeto ou adicionar quaisquer detalhes adicionais conforme necessário!