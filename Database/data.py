import json
import os
import uuid
from typing import Optional

class Base():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_file = './Database/collections.json'
        self.collections = self.load_data()
        self.users_data_file = './Database/users.json'
        self.users = self.load_user_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return {'collections': []}

    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.collections, f, indent=4)

    def load_user_data(self):
        if os.path.exists(self.users_data_file):
            with open(self.users_data_file, 'r') as f:
                return json.load(f)
        return {}

    def save_user_data(self):
        with open(self.users_data_file, 'w') as f:
            json.dump(self.users, f, indent=4)


    async def add_collection(self, name: str):
        collection_id = str(uuid.uuid4())
        self.collections['collections'].append({'id': collection_id, 'name': name, 'cards': []})
        self.save_data()
        return collection_id

    async def add_card(self, collection_id: str, name: str, rarity: str, image_url: Optional[str]):
        id= uuid.uuid4()
        card = {
            'id': str(id),
            'collection_id': collection_id,
            'name': name,
            'rarity': rarity,
            'image_url': image_url
        }
        for collection in self.collections['collections']:
            if collection['id'] == collection_id:
                collection['cards'].append(card)
                self.save_data()
                return id
        raise ValueError('Collection not found')

    async def get_collection_by_name(self, name: str):
        for collection in self.collections['collections']:
            if collection['name'].lower() == name.lower():
                return collection
        return None

    async def check_collection_completion(self, user_id: str, collection_id: str):
        user_cards = self.users.get(str(user_id), {}).get('cards', {})
        for collection in self.collections['collections']:
            if collection['id'] == collection_id:
                collection_card_ids = {card['id'] for card in collection['cards']}
                user_card_ids = set(user_cards.get(collection_id, []))
                return collection_card_ids <= user_card_ids
        return False

    async def has_claimed_reward(self, user_id: str, collection_id: str):
        return collection_id in self.users.get(str(user_id), {}).get('claimed_rewards', [])

    async def claim_reward(self, user_id: str, collection_id: str):
        if str(user_id) not in self.users:
            self.users[str(user_id)] = {'cards': {}, 'claimed_rewards': []}
        self.users[str(user_id)]['claimed_rewards'].append(collection_id)
        self.save_user_data()

    async def get_cards_by_rarity(self, rarity: str):
        cards = []
        for collection in self.collections['collections']:
            for card in collection['cards']:
                if card['rarity'] == rarity:
                    cards.append(card)
        return cards

    async def get_user_cards_by_collection(self, user_id: str, collection_id: str):
        user_cards = self.users.get(str(user_id), {}).get('cards', {})
        return user_cards.get(collection_id, [])
        
        
        
    async def get_user_cards_by_rarity(self, user_id: str, rarity: str):
        user_cards = self.users.get(str(user_id), {}).get('cards', {})
        cards = []
        for collection in self.collections['collections']:
            for card in collection['cards']:
                if card['rarity'] == rarity and card['id'] in user_cards.get(collection['id'], []):
                    cards.append(card)
        return cards


    async def add_card_to_user(self, user_id: str, card_id: str):
        if str(user_id) not in self.users:
            self.users[str(user_id)] = {'cards': {}, 'claimed_rewards': []}
        for collection in self.collections['collections']:
            for card in collection['cards']:
                if card['id'] == card_id:
                    if collection['id'] not in self.users[str(user_id)]['cards']:
                        self.users[str(user_id)]['cards'][collection['id']] = []
                    self.users[str(user_id)]['cards'][collection['id']].append(card_id)
                    self.save_user_data()
                    return
                

    async def get_user_cards(self, user_id: str):
        user_cards = []
        user_data = self.users.get(str(user_id), {}).get('cards', {})

        for collection_id, card_ids in user_data.items():
            collection = await self.get_collection(collection_id)
            if collection:
                for card_id in card_ids:
                    for card in collection['cards']:
                        if card['id'] == card_id:
                            user_cards.append(card)
        
        return user_cards
    
    

    async def count_users_with_card(self, card_id: str):
        count = 0
        for user_data in self.users.values():
            for collection_cards in user_data.get('cards', {}).values():
                if card_id in collection_cards:
                    count += 1
        return count

    async def get_all_collections(self):
        return self.collections['collections']

    async def get_collection(self, collection_id: str):
        for collection in self.collections['collections']:
            if collection['id'] == collection_id:
                return collection
        return None

    async def get_cards_by_collection(self, collection_id: str):
        for collection in self.collections['collections']:
            if collection['id'] == collection_id:
                return collection['cards']
        return []

    async def card_exists_in_user(self, card_id: str, user_id: str):
        user_cards = self.users.get(str(user_id), {}).get('cards', {})
        for card_ids in user_cards.values():
            if card_id in card_ids:
                return True
        return False
    
    async def get_collection_by_name(self, name: str):
            for collection in self.collections['collections']:
                if collection['name'].lower() == name.lower():
                    return collection
            return None
        
        
        



