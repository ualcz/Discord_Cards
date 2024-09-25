import mysql.connector
import uuid
from typing import Optional






class Base():
    def __init__(self, db_config):
        self.connection = mysql.connector.connect(**db_config)
        self.cursor = self.connection.cursor()
        self.connection.commit()

    async def add_collection(self, name: str):
        collection_id = str(uuid.uuid4())
        self.cursor.execute("INSERT INTO collections (id, name) VALUES (%s, %s)", (collection_id, name))
        self.connection.commit()
        return collection_id

    async def add_card(self, collection_id: str, name: str, rarity: str, image_url: Optional[str]):
        card_id = str(uuid.uuid4())
        try:
            self.cursor.execute(
                "INSERT INTO cards (id, collection_id, name, rarity, image_url) VALUES (%s, %s, %s, %s, %s)",
                (card_id, collection_id, name, rarity, image_url)
            )
            self.connection.commit()  # Certifique-se de que o commit está aqui
            print(f"Card {card_id} adicionado com sucesso.")
            return card_id
        except Exception as e:
            print(f"Erro ao adicionar card: {e}")
            return None

    async def get_collection_by_name(self, name: str):
        self.cursor.execute("SELECT * FROM collections WHERE LOWER(name) = LOWER(%s)", (name,))
        return self.cursor.fetchone()

    async def check_collection_completion(self, user_id: str, collection_id: str):
        self.cursor.execute("SELECT card_id FROM user_cards WHERE user_id = %s", (user_id,))
        user_card_ids = {row[0] for row in self.cursor.fetchall()}
        
        self.cursor.execute("SELECT id FROM cards WHERE collection_id = %s", (collection_id,))
        collection_card_ids = {row[0] for row in self.cursor.fetchall()}
        
        return collection_card_ids <= user_card_ids

    async def has_claimed_reward(self, user_id: str, collection_id: str):
        self.cursor.execute("SELECT * FROM claimed_rewards WHERE user_id = %s AND collection_id = %s", (user_id, collection_id))
        return self.cursor.fetchone() is not None

    async def claim_reward(self, user_id: str, collection_id: str):
        self.cursor.execute("INSERT INTO claimed_rewards (user_id, collection_id) VALUES (%s, %s)", (user_id, collection_id))
        self.connection.commit()

    async def get_cards_by_rarity(self, rarity: str):
        self.cursor.execute("SELECT * FROM cards WHERE rarity = %s", (rarity,))
        return self.cursor.fetchall()

    async def get_user_cards_by_collection(self, user_id: str, collection_id: str):
        self.cursor.execute("""
            SELECT c.* FROM cards c
            JOIN user_cards uc ON c.id = uc.card_id
            WHERE uc.user_id = %s AND c.collection_id = %s
        """, (user_id, collection_id))
        return self.cursor.fetchall()

    async def add_card_to_user(self, user_id: str, card_id: str):
        self.cursor.execute("INSERT IGNORE INTO users (id) VALUES (%s)", (user_id,))
        self.cursor.execute("INSERT INTO user_cards (user_id, card_id) VALUES (%s, %s)", (user_id, card_id))
        self.connection.commit()

    async def get_user_cards(self, user_id: str):
        self.cursor.execute("""
            SELECT c.* FROM cards c
            JOIN user_cards uc ON c.id = uc.card_id
            WHERE uc.user_id = %s
        """, (user_id,))
        return self.cursor.fetchall()

    async def count_users_with_card(self, card_id: str):
        self.cursor.execute("SELECT COUNT(DISTINCT user_id) FROM user_cards WHERE card_id = %s", (card_id,))
        return self.cursor.fetchone()[0]

    async def get_all_collections(self):
        self.cursor.execute("SELECT * FROM collections") 
        return self.cursor.fetchall()

    async def get_collection(self, collection_id: str):
        self.cursor.execute("SELECT * FROM collections WHERE id = %s", (collection_id,))
        return self.cursor.fetchone()

    async def get_cards_by_collection(self, collection_id: str):
        self.cursor.execute("SELECT * FROM cards WHERE collection_id = %s", (collection_id,))
        return self.cursor.fetchall()

    async def card_exists_in_user(self, card_id: str, user_id: str):
        self.cursor.execute("SELECT * FROM user_cards WHERE user_id = %s AND card_id = %s", (user_id, card_id))
        return self.cursor.fetchone() is not None

    async def close(self):
        self.cursor.close()
        self.connection.close()

