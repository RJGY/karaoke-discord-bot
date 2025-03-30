import discord
from discord import SelectOption
from discord.ui import Select, Button, View
import datetime as dt
import requests
import os
import logging
import validators
from pytubefix import Search
import pytubefix

from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
api_host = os.getenv('API_HOST')

class KaraokeCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    """Listeners"""
    @commands.Cog.listener()
    async def on_ready(self):
        synced = await self.bot.tree.sync()
        for command in synced:
            logging.info(f'Synced {command.name} with slash commands.')
        logging.info(f'Synced {len(synced)} commands with slash commands.')

            
    """Commands"""
    @discord.app_commands.command(name='test', description='Test command to make sure im not going insane :3.')
    async def test_command(self, interaction: discord.Interaction):
        await interaction.response.send_message('Test command.')

        
    @discord.app_commands.command(name='play', description='Plays a song')
    @discord.app_commands.describe(song='The user to retrieve info from.')
    async def play_command(self, interaction: discord.Interaction, song: str):
        await interaction.response.defer()

        if not song:
            embed = discord.Embed(
                title='Error',
                colour=discord.Colour.red(),    
                timestamp=dt.datetime.now()
            )
            embed.set_author(name='Karaoke Bot')
            embed.add_field(name=f'No song was given.', value='')
            await interaction.followup.send(embed=embed)
            return
        
        song_url = song
        
        if not validators.url(song_url):
            videos = Search(song_url).videos[:10]
            selection_options = []
            embed_text = ""

            for i, video in enumerate(videos):
                embed_text += f"{i+1} - [{video.title}]({video.watch_url})\n"
                selection_options.append(SelectOption(label=f"{i+1} - {video.title[:95]}", value=i))

            search_results_embed = discord.Embed(
                title="Search Results",
                description=embed_text,
                colour=discord.Colour.blue(),
                timestamp=dt.datetime.now()
            )

            class SearchView(View):
                def __init__(self):
                    super().__init__(timeout=30)
                    self.message = None

                async def on_timeout(self):
                    # Create timeout embed
                    timeout_embed = discord.Embed(
                        title='Search Timed Out',
                        description='Song selection has timed out. Please try again.',
                        colour=discord.Colour.red(),
                        timestamp=dt.datetime.now()
                    )
                    
                    # Disable all items in the view
                    for item in self.children:
                        item.disabled = True
                    
                    # Update the message with disabled view and new embed
                    await self.message.edit(embed=timeout_embed, view=self)

                @discord.ui.select(placeholder="Select an option", options=selection_options)
                async def select_callback(self, interaction: discord.Interaction, select: Select):
                    selected_video = videos[int(select.values[0])]
                    selection_embed = discord.Embed(
                        title='Song Selected',
                        description=f'Selected: [{selected_video.title}]({selected_video.watch_url})',
                        colour=discord.Colour.green(),
                        timestamp=dt.datetime.now(),
                    )
                    selection_embed.set_thumbnail(url=selected_video.thumbnail_url)
                    
                    # Disable all items in the view
                    for item in self.children:
                        item.disabled = True
                    
                    # Update the message with disabled view and new embed
                    await interaction.response.edit_message(embed=selection_embed, view=self)

                    try:
                        requests.post(f'{api_host}/api/queue', data=data)
                    except Exception as e:
                        embed = discord.Embed(
                            title='Error',
                            colour=discord.Colour.red(),    
                            timestamp=dt.datetime.now()
                        )
                        embed.set_author(name='Karaoke Bot')
                        embed.add_field(name=f'Could not connect to server.', value='')
                        logging.error(f'Unable to connect to server: {e}')
                        await interaction.followup.send(embed=embed)
                        return

                    # Send queueing status embed as a follow-up
                    queue_embed = discord.Embed(
                        title='Song Queued',
                        colour=discord.Colour.blue(),
                        timestamp=dt.datetime.now()
                    )
                    queue_embed.set_thumbnail(url=interaction.user.display_avatar)
                    queue_embed.set_author(name='Karaoke Bot')
                    queue_embed.add_field(
                        name=f'{interaction.user.display_name} has requested {selected_video.title}', 
                        value='', 
                        inline=False
                    )
                    queue_embed.set_image(url=selected_video.thumbnail_url)
                    queue_embed.set_footer(text=f'{interaction.user.display_name}')
                    await interaction.followup.send(embed=queue_embed)

                @discord.ui.button(label='Cancel', custom_id='cancel')
                async def cancel_button(self, interaction: discord.Interaction, button: Button):
                    cancel_embed = discord.Embed(
                        title='Search Cancelled',
                        description='Song selection has been cancelled.',
                        colour=discord.Colour.red(),
                        timestamp=dt.datetime.now()
                    )
                    
                    # Disable all items in the view
                    for item in self.children:
                        item.disabled = True
                    
                    # Update the message with disabled view and new embed
                    await interaction.response.edit_message(embed=cancel_embed, view=self)

            view = SearchView()

            message = await interaction.followup.send(embed=search_results_embed, view=view)
            view.message = message
        else:
            video = pytubefix.YouTube(song_url)

            data = {
                'url' : song_url
            }

            try:
                requests.post(f'{api_host}/api/queue', data=data)
            except Exception as e:
                embed = discord.Embed(
                    title='Error',
                    colour=discord.Colour.red(),    
                    timestamp=dt.datetime.now()
                )
                embed.set_author(name='Karaoke Bot')
                embed.add_field(name=f'Could not connect to server.', value='')
                logging.error(f'Unable to connect to server: {e}')
                await interaction.followup.send(embed=embed)
                return
            
            embed = discord.Embed(
                title='Song Queued',
                colour=discord.Colour.blue(),
                timestamp=dt.datetime.now()
            )
            embed.set_thumbnail(url=interaction.user.display_avatar)
            embed.set_image(url=video.thumbnail_url)
            embed.set_author(name='Karaoke Bot')
            embed.add_field(name=f'{interaction.user.display_name} has requested {video.title}', value='', inline=False)
            embed.set_footer(text=f'{interaction.user.display_name}')
            await interaction.followup.send(embed=embed)
            

    @commands.hybrid_command(name='sync', description='Syncs the bot with slash commands.')
    async def sync_command(self, ctx: commands.Context):
        """Syncs the bot with slash commands."""
        await ctx.defer()
        synced = await self.bot.tree.sync()
        for command in synced:
            await ctx.send(f'Synced {command.name} with slash commands.')
        await ctx.send(f'Synced {len(synced)} commands with slash commands.')
            
        
async def setup(bot: commands.Bot):
    await bot.add_cog(KaraokeCommands(bot))
    
    

if __name__ == '__main__':
    pass