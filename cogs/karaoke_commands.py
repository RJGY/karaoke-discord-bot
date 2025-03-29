import discord
from discord.ext import commands
import datetime as dt

class KaraokeCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
            
    """Commands"""
    @discord.app_commands.command(name="test", description="Test command to make sure im not going insane :3.")
    async def test_command(self, interaction: discord.Interaction):
        await interaction.response.send_message("Test command.")
        
    @discord.app_commands.command(name="play", description="Plays a song")
    @discord.app_commands.describe(song="The user to retrieve info from.")
    async def play_command(self, interaction: discord.Interaction, song: str):
        await interaction.response.defer()

        if not song:
            embed = discord.Embed(
                title="Error",
                colour=discord.Colour.red(),    
                timestamp=dt.datetime.now()
            )
            embed.set_author(name="Karaoke Bot")
            embed.add_field(name=f'No song was given.', value='')
            await interaction.followup.send(embed=embed)
            return

        # TODO here is where i need to fire a webreq or something
        
        embed = discord.Embed(
            title="Song Queued",
            colour=discord.Colour.blue(),
            timestamp=dt.datetime.now()
        )
        embed.set_thumbnail(url=interaction.user.display_avatar)
        embed.set_author(name="Karaoke Bot")
        embed.add_field(name=f'{interaction.user.display_name} has requested {song}', value='', inline=False)
        embed.set_footer(text=f'{interaction.user.display_name}')
        await interaction.followup.send(embed=embed)

    @commands.hybrid_command(name="sync", description="Syncs the bot with slash commands.")
    async def sync_command(self, ctx: commands.Context):
        """Syncs the bot with slash commands."""
        await ctx.defer()
        synced = await self.bot.tree.sync()
        for command in synced:
            await ctx.send(f"Synced {command.name} with slash commands.")
        await ctx.send(f"Synced {len(synced)} commands with slash commands.")
            
        
async def setup(bot: commands.Bot):
    await bot.add_cog(KaraokeCommands(bot))
    
    

if __name__ == "__main__":
    pass