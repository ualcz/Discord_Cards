import discord
from config import *


class CollectionPaginationView(discord.ui.View):
    def __init__(self, collections, user):
        super().__init__()
        self.collections = collections
        self.user = user
        self.current_collection_index = 0
        self.current_card_index = 0

    @discord.ui.button(label=' ',emoji=emoji.get('angleleft'), style=discord.ButtonStyle.blurple)
    async def previous_card(self, interaction: discord.Interaction, button: discord.ui.Button):
        collection = self.collections[self.current_collection_index]
        collection_id = collection[0]
        cards = await interaction.client.database.get_cards_by_collection(collection_id)
        
        if self.current_card_index > 0:
            self.current_card_index -= 1
        else:
            self.current_card_index=len(cards)- 1
        await self.update_message(interaction)

    @discord.ui.button(label=' ',emoji= emoji.get('angleright'), style=discord.ButtonStyle.blurple)
    async def next_card(self, interaction: discord.Interaction, button: discord.ui.Button):
        collection = self.collections[self.current_collection_index]
        collection_id = collection[0]
        cards = await interaction.client.database.get_cards_by_collection(collection_id)

        if self.current_card_index < len(cards) - 1:
            self.current_card_index += 1
        else:
            self.current_card_index=0
        await self.update_message(interaction)

    @discord.ui.button(label=' ',emoji= emoji.get('book'), style=discord.ButtonStyle.green)
    async def change_collection(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_collection_index < len(self.collections) - 1:
            self.current_collection_index += 1
        else:
            self.current_collection_index = 0
        self.current_card_index = 0
        await self.update_message(interaction)
    
        
        
    @discord.ui.button(label=' ',emoji= emoji.get('info'), style=discord.ButtonStyle.grey)
    async def info(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.show_card_info(interaction)


    async def update_message(self, interaction: discord.Interaction):
        
        collection = self.collections[self.current_collection_index]
        collection_id = collection[0]
        collection_name = collection[1]
        cards = await interaction.client.database.get_cards_by_collection(collection_id)
        
        if not cards:
            discord.Embed(title=f"Nenhum card disponível na coleção '{collection[1]}'.", color=color['coletion_color'])
            await interaction.response.edit_message(embed=embed, view=self)
            return

        card = cards[self.current_card_index]
        
        embed = discord.Embed(title=f"Card na Coleção '{collection['name']}'\n({self.current_card_index + 1}/{len(cards)})", color=color[card[3]])
        embed.add_field(name="Nome", value=card[1], inline=False)
        embed.add_field(name="Raridade", value=rarity_to_emoji.get(card[3]), inline=False)
        embed.set_thumbnail(url=card['image_url'])
        
        await interaction.response.edit_message(embed=embed, view=self)
        
    async def show_card_info(self, interaction: discord.Interaction):
        collection = self.collections[self.current_collection_index]
        collection_id = collection[0]
        all_cards = await interaction.client.database.get_cards_by_collection(collection_id)
        card = all_cards[self.current_card_index]

        collection = await interaction.client.database.get_collection(card[1])
        count_users = await interaction.client.database.count_users_with_card(card[0])

        embed = discord.Embed(title=f"Info: {card[2]}", color=color[card[3]])
        embed.set_image(url=card['image_url'])
        embed.add_field(name="Raridade", value=rarity_to_emoji.get(card[3]), inline=False)
        embed.add_field(name="Coleção", value=collection[1], inline=False)
        embed.add_field(name="Usuários", value=count_users, inline=True)
        await interaction.response.send_message(embed=embed, ephemeral=True)


    async def get_initial_embed(self, interaction: discord.Interaction):
        collection = self.collections[self.current_collection_index]
        collection_id = collection[0]
        collection_name = collection[1]

        cards = await interaction.client.database.get_cards_by_collection(collection_id)
        if not cards:
            return discord.Embed(title=f"Nenhum card disponível na coleção '{collection[1]}'.", color=color['coletion_color'])

        card = cards[self.current_card_index]

        embed = discord.Embed(title=f"Card na Coleção '{collection[1]}\n({self.current_card_index + 1}/{len(card)})'", color=color[card[3]])
        embed.add_field(name="Nome", value=card[2], inline=False)
        embed.add_field(name="Raridade", value=rarity_to_emoji.get(card[3]), inline=False)
        embed.set_thumbnail(url=card[4])

        return embed





class UserCollectionPaginationView(discord.ui.View):
    def __init__(self, collections, user,):
        super().__init__()
        self.collections = collections
        self.user_id = user.id
        self.user = user
        self.current_collection_index = 0
        self.current_card_index = 0
        self.detailed_view = False  # Flag to switch between overview and detailed view

    @discord.ui.button(label=' ', emoji=emoji.get('angleleft'), style=discord.ButtonStyle.blurple)
    async def previous_card(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.detailed_view:
            collection = self.collections[self.current_collection_index]
            collection_id = collection[0]
            cards = await interaction.client.database.get_cards_by_collection(collection_id)

            if self.current_card_index > 0:
                self.current_card_index -= 1
            else:
                self.current_card_index = len(cards) - 1
                
            await self.update_message(interaction)
            
        else:
            self.current_card_index = 0
            if self.current_collection_index > 0:
                self.current_collection_index -= 1
            else:
                self.current_collection_index = len(self.collections) - 1

            await self.show_collection_overview(interaction)

    @discord.ui.button(label=' ', emoji=emoji.get('angleright'), style=discord.ButtonStyle.blurple)
    async def next_card(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.detailed_view:
            collection = self.collections[self.current_collection_index]
            collection_id = collection[0]
            cards = await interaction.client.database.get_cards_by_collection(collection_id)

            if self.current_card_index < len(cards) - 1:
                self.current_card_index += 1
            else:
                self.current_card_index = 0
                
            await self.update_message(interaction)
            
        else:
            self.current_card_index = 0
            if self.current_collection_index < len(self.collections) - 1:
                self.current_collection_index += 1
            else:
                self.current_collection_index = 0

            await self.show_collection_overview(interaction)

    @discord.ui.button(label=' ', emoji=emoji.get('book'), style=discord.ButtonStyle.green)
    async def change_collection(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.detailed_view = not self.detailed_view
        if self.detailed_view:
            await self.update_message(interaction)
        else:
            await self.show_collection_overview(interaction)

    @discord.ui.button(label=' ', emoji=emoji.get('info'), style=discord.ButtonStyle.grey)
    async def info(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.show_card_info(interaction)

    async def update_message(self, interaction: discord.Interaction):
        collection = self.collections[self.current_collection_index]
        collection_id = collection[0]
        all_cards = await interaction.client.database.get_cards_by_collection(collection_id)
        user_card_ids = await interaction.client.database.get_user_cards_by_collection(self.user_id, collection_id)

        card = all_cards[self.current_card_index]

        embed = discord.Embed(title=f"Card '{collection[1]}' by {self.user.name} \n({self.current_card_index + 1}/{len(all_cards)})", color=color[card[3]])
        embed.set_thumbnail(url=card[4])
        embed.add_field(name="Nome", value=card[2], inline=False)
        embed.add_field(name="Raridade", value=rarity_to_emoji.get(card[3]), inline=False)

        if card[0] in user_card_ids:
            embed.add_field(name="Status", value="Coletado", inline=False)
        else:
            embed.add_field(name="Status", value="Pendente", inline=False)

        # Calcular quantos cards faltam para o usuário completar a coleção
        total_cards = len(all_cards)
        cards_faltando = total_cards - len(user_card_ids)
        embed.add_field(name="Faltam", value=f"{cards_faltando} cards para completar a coleção", inline=False)

        await interaction.response.edit_message(embed=embed, view=self)

    async def show_card_info(self, interaction: discord.Interaction):
        collection = self.collections[self.current_collection_index]
        collection_id = collection[0]
        all_cards = await interaction.client.database.get_cards_by_collection(collection_id)
        card = all_cards[self.current_card_index]

        collection = await interaction.client.database.get_collection(card[1])
        count_users = await interaction.client.database.count_users_with_card(card[0])

        embed = discord.Embed(title=f"Info: {card[2]}", color=color[card[3]])
        embed.set_image(url=card[4])
        embed.add_field(name="Raridade", value=rarity_to_emoji.get(card[3]), inline=False)
        embed.add_field(name="Coleção", value=collection[1], inline=False)
        embed.add_field(name="Usuários", value=count_users, inline=True)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def show_collection_overview(self, interaction: discord.Interaction):
        collection = self.collections[self.current_collection_index]
        collection_id = collection[0]

        all_cards = await interaction.client.database.get_cards_by_collection(collection_id)
        user_cards = await interaction.client.database.get_user_cards_by_collection(self.user_id, collection_id)

        embed = discord.Embed(title=f"Coleção: {collection[1]} \n({self.current_collection_index + 1}/{len(self.collections)})", color=discord.Color.blue())
        embed.set_thumbnail(url=self.user.avatar)
        embed.add_field(name="Total de Cartões:", value=len(all_cards), inline=False)
        embed.add_field(name=f"Coletados:", value=f'{len(user_cards)} ', inline=False)
        embed.add_field(name="Progresso:", value=f"{len(user_cards)}/{len(all_cards)}", inline=False)

        await interaction.response.edit_message(embed=embed, view=self)

    async def get_initial_embed(self, interaction: discord.Interaction):
        collection = self.collections[self.current_collection_index]
        collection_id = collection[0]

        all_cards = await interaction.client.database.get_cards_by_collection(collection_id)
        user_cards = await interaction.client.database.get_user_cards_by_collection(self.user_id, collection_id)

        embed = discord.Embed(title=f"Card '{collection[1]}' by {self.user.name} \n({self.current_collection_index + 1}/{len(self.collections)})", color=discord.Color.blue())
        embed.set_thumbnail(url=self.user.avatar)
        embed.add_field(name="Total de Cartões:", value=len(all_cards), inline=False)
        embed.add_field(name=f"Coletados:", value=f'{len(user_cards)} ', inline=False)
        embed.add_field(name="Progresso:", value=f"{len(user_cards)}/{len(all_cards)}", inline=False)

        return embed

