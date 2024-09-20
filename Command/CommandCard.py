import discord
import random
from config import *
from typing import Literal, Optional
from discord import app_commands
from View.CardView import CollectionPaginationView, UserCollectionPaginationView

class CommandCard:
    def __init__(self, client):
        self.client = client

    def setup(self):
        
        
        '''Funções exclusivas comandos relacionados à adição de coleções e cards'''
        @self.client.tree.command()
        async def add_collection(interaction: discord.Interaction, name: str):
            """Adiciona uma nova coleção."""
            collection_id = await self.client.database.add_collection(name)
            await interaction.response.send_message(f"Coleção '{name}' adicionada com ID '{collection_id}'.", ephemeral=True)

        @self.client.tree.command()
        async def add_card(interaction: discord.Interaction,
                        collection: str,
                        name: str,
                        rarity: Literal['Common', 'Uncommon', 'Rare', 'Epic', 'Legendary'],
                        image_url: Optional[str] = None):
            """Adiciona um novo card a uma coleção."""
            try:
                # Buscar a coleção pelo nome
                collection_data = await self.client.database.get_collection_by_name(collection)
                if not collection_data:
                    await interaction.response.send_message("Coleção não encontrada.", ephemeral=True)
                    return

                # Adicionar o card à coleção encontrada
                card_id = await self.client.database.add_card(collection_data['id'], name, rarity, image_url)
                
                # Criar embed com informações do card
                embed = discord.Embed(title=f"Card adicionado com sucesso", color=color[rarity])
                embed.set_thumbnail(url=image_url)
                embed.add_field(name="Nome", value=name, inline=False)
                embed.add_field(name="Coleção", value=collection, inline=False)
                embed.add_field(name="Raridade", value=rarity_to_emoji.get(rarity), inline=True)
                
                await interaction.response.send_message(embed=embed, ephemeral=False)
            
            except ValueError as e:
                await interaction.response.send_message(str(e), ephemeral=True)

            
                
        # Comando para reivindicar recompensa
        @self.client.tree.command()
        async def claim_reward(interaction: discord.Interaction, collection_name: str):
            """Reivindica a recompensa por completar uma coleção."""
            try:
                collection = await self.client.database.get_collection_by_name(collection_name)
                if not collection:
                    await interaction.response.send_message("Coleção não encontrada.", ephemeral=True)
                    return

                user_id = interaction.user.id
                collection_id = collection['id']
                collection_complete = await self.client.database.check_collection_completion(user_id, collection_id)

                if not collection_complete:
                    await interaction.response.send_message("Você ainda não completou esta coleção.", ephemeral=True)
                    return

                has_claimed = await self.client.database.has_claimed_reward(user_id, collection_id)
                if has_claimed:
                    await interaction.response.send_message("Você já reivindicou a recompensa para esta coleção.", ephemeral=True)
                    return

                await self.client.database.claim_reward(user_id, collection_id)
                await interaction.response.send_message(f"Recompensa reivindicada com sucesso!", ephemeral=True)
            except Exception as e:
                print(f"Error in claim_reward: {e}")
                await interaction.response.send_message("Ocorreu um erro, tente novamente mais tarde", ephemeral=True)
                    

                # Comando para listar cards de uma coleção específica
        @self.client.tree.command()
        async def collections(interaction: discord.Interaction, collection_name: Optional[str] = None):
                    """Lista todas as coleções ou cards de uma coleção específica."""
                    try:
                        collections = await self.client.database.get_all_collections()
                        if not collections:
                            await interaction.response.send_message("Nenhuma coleção encontrada.", ephemeral=True)
                            return

                        collection = None
                        if collection_name:
                            collection = next((col for col in collections if col['name'].lower() == collection_name.lower()), None)
                            if not collection:
                                await interaction.response.send_message("Coleção não encontrada.", ephemeral=True)
                                return
                            collections = [collection]

                        view = CollectionPaginationView(collections, interaction.user)
                        embed = await view.get_initial_embed(interaction)  # Get the initial embed to display
                        await interaction.response.send_message(embed=embed, view=view, ephemeral=False)

                    except Exception as e:
                        print(f"Error in collections: {e}")
                        await interaction.response.send_message("Ocorreu um erro, tente novamente mais tarde", ephemeral=True)


        @self.client.tree.command()
        async def user_info(interaction: discord.Interaction, collection_name: Optional[str] = None, member: Optional[discord.Member] = None):
            """Lista os cards de um usuário em uma coleção específica."""
            try:
                user = member or interaction.user
                user_id = user.id

                collections = await self.client.database.get_all_collections()
                if not collections:
                    await interaction.response.send_message("Nenhuma coleção encontrada.", ephemeral=True)
                    return

                if collection_name:
                    collection = next((col for col in collections if col['name'].lower() == collection_name.lower()), None)
                    if not collection:
                        await interaction.response.send_message("Coleção não encontrada.", ephemeral=True)
                        return
                    collections = [collection]

                view = UserCollectionPaginationView(collections, user)
                embed = await view.get_initial_embed(interaction)  # Get the initial embed to display
                await interaction.response.send_message(embed=embed, view=view, ephemeral=False)
            except Exception as e:
                print(f"Error in user_info: {e}")
                await interaction.response.send_message("Ocorreu um erro, tente novamente mais tarde", ephemeral=True)





        @self.client.tree.command()
        @app_commands.checks.cooldown(1, 10)
        async def collect(interaction: discord.Interaction):
            """Coleta um card aleatório com base na raridade."""
            try:
                user_id = interaction.user.id
                
                all_collections = await self.client.database.get_all_collections()
                user_cards = await self.client.database.get_user_cards(user_id)
                
                if not all_collections:
                    await interaction.response.send_message("Não há coleções disponíveis.", ephemeral=True)
                    return
                
                # Filtrar cartões que o usuário ainda não possui
                available_cards = []
                for collection in all_collections:
                    for card in collection['cards']:
                        card_not= await self.client.database.card_exists_in_user(card['id'],user_id)
                        if not card_not:
                            available_cards.append(card)

                if not available_cards:
                    await interaction.response.send_message("Você já possui todos os cards disponíveis.", ephemeral=True)
                    return

                while True:
                    rarity = random.choices(list(RARITY_PROBABILITIES.keys()), weights=list(RARITY_PROBABILITIES.values()), k=1)[0]
                    cards_by_rarity = [card for card in available_cards if card['rarity'] == rarity]

                    if not cards_by_rarity:
                        continue  # Tenta novamente se não houver cards dessa raridade que o usuário não possui
                    
                    card = random.choice(cards_by_rarity)
                    
                    collection = await self.client.database.get_collection(card['collection_id'])
                    if not collection:
                        await interaction.response.send_message("Coleção não encontrada para este card.", ephemeral=True)
                        return

                    embed = discord.Embed(title=f"Card {card['name']} coletado:", color=color[rarity])
                    embed.set_thumbnail(url=card['image_url'])
                    embed.add_field(name="Coleção", value=collection['name'], inline=False)
                    embed.add_field(name="Raridade", value=rarity_to_emoji.get(card['rarity']), inline=True)

                    await self.client.database.add_card_to_user(user_id, card['id'])

                    count_users = await self.client.database.count_users_with_card(card['id'])
                    embed.add_field(name="Usuários", value=count_users, inline=True)

                    collection_complete = await self.client.database.check_collection_completion(user_id, card['collection_id'])
                    if collection_complete:
                        embed.add_field(name="Coleção Completa", value="Você completou a coleção! Reivindique sua recompensa com /claim_reward.", inline=False)

                    await interaction.response.send_message(embed=embed, ephemeral=False)
                    break

            except Exception as e:
                print(f"Error in collect: {e}")
                await interaction.response.send_message("Ocorreu um erro, tente novamente mais tarde", ephemeral=True)
                
                
                
                
                
                
                
                
                
