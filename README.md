
# Bot de Jogo de Cartas do Discord

Bem-vindo ao **Bot de Jogo de Cartas do Discord**! Este bot permite que os usuários colecione cartas e receba recompensa para cada card colecionado.

---
## 🛠️ Requisitos

Antes de começar, certifique-se de ter o seguinte:

- Python 3.8 ou superior
- Biblioteca Discord.py (Instale usando `pip install discord.py`)
- Um Token de Bot do Discord
- Banco de dados PostgreSQL ou outro SGBD compatível

## 🔧 Configuração

1. **Clone o Repositório**:

   ```bash
   git clone https://github.com/ualcz/Discord_Cards.git
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
![Descrição da Imagem](./Img/IMG1.png)
- `/user_info`:Lista os cards de um usuário.
![Descrição da Imagem](./Img/IMG4.png)


---

## 📊 Estrutura do Banco de Dados

Aqui está a estrutura básica do banco de dados usada pelo bot para armazenar informações dos usuários e coleções de cartas.

### Tabela: `users`

```sql
CREATE TABLE users (
	`id` VARCHAR(50) NOT NULL,
   `username` VARCHAR(100) NOT NULL,
   `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
	PRIMARY KEY (`id`) USING BTREE
);

```

### Tabela: `collections`

```sql
CREATE TABLE `collections` (
	`id` VARCHAR(50) NOT NULL DEFAULT,
	`name` VARCHAR(50) NULL DEFAULT NULL,
	PRIMARY KEY (`id`) USING BTREE,
	INDEX `name` (`name`) USING BTREE
);
```

### Tabela: `cards`

```sql
CREATE TABLE `cards` (
	`id` CHAR(50) NOT NULL ,
	`collection_id` VARCHAR(50) NOT NULL ,
	`name` CHAR(50) NULL DEFAULT NULL ,
	`rarity` VARCHAR(50) NULL DEFAULT NULL ,
	`image_url` TEXT NULL DEFAULT NULL ,
	PRIMARY KEY (`id`) USING BTREE,
	INDEX `FK_cards_collections` (`collection_id`) USING BTREE,
	CONSTRAINT `FK_cards_collections` FOREIGN KEY (`collection_id`) REFERENCES `collections` (`id`) ON UPDATE NO ACTION ON DELETE NO ACTION
);

```

### Tabela: `user_cards`

```sql
CREATE TABLE `user_cards` (
	`card_id` CHAR(50) NULL DEFAULT NULL,
	`user_id` VARCHAR(50) NULL DEFAULT NULL ,
	INDEX `FK__cards` (`card_id`) USING BTREE,
	INDEX `FK__users` (`user_id`) USING BTREE,
	CONSTRAINT `FK__cards` FOREIGN KEY (`card_id`) REFERENCES `cards` (`id`) ON UPDATE NO ACTION ON DELETE NO ACTION,
	CONSTRAINT `FK__users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON UPDATE NO ACTION ON DELETE NO ACTION
);
```

---
## 📄 Licença

Este projeto está licenciado sob a Licença MIT - consulte o arquivo [LICENSE](LICENSE) para mais detalhes.

---
Contribuições são bem-vindas! Se você tiver sugestões para melhorias ou novos recursos, por favor, abra uma issue ou envie uma solicitação de pull ou entre em contato com [Clau] em [Claudeilsonsouzza@gmail.com] para mais informações.