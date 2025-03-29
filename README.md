# Discord Karaoke Bot

A Discord bot that helps manage karaoke sessions in your server. This bot allows users to queue songs and interact with karaoke sessions through Discord commands.

## Features

- 🎵 Play command to queue songs
- 🎮 Slash command support
- 🔄 Automatic command syncing
- 📝 Detailed logging system
- ⚡ Fast and responsive

## Setup

1. Clone the repository:
```bash
git clone https://github.com/rjgy/karaoke-discord-bot.git
cd karaoke-discord-bot
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with the following variables:
```env
DISCORD_TOKEN=your_discord_bot_token
SYMBOL=your_command_prefix
API_HOST=your_api_host
```

4. Run the bot:
```bash
python main.py
```

## Usage

### Commands

- `/play <song>` - Queue a song for karaoke
- `/sync` - Sync slash commands with Discord
- `/test` - Test command to verify bot functionality

### Example Usage

```
/play Bohemian Rhapsody
```

## Dependencies

- discord.py
- python-dotenv
- logging

## Configuration

The bot uses environment variables for configuration:
- `DISCORD_TOKEN`: Your Discord bot token
- `SYMBOL`: The command prefix for traditional commands
