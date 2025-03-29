# Discord Karaoke Bot

A Discord bot that helps manage karaoke sessions in your server. This bot allows users to queue songs and interact with karaoke sessions through Discord commands.

## Features

- 🎵 Song queuing with YouTube support
- 🔍 Interactive song search with up to 10 results
- 🎮 Slash command support
- 🔄 Automatic command syncing
- 📝 Detailed logging system
- ⚡ Fast and responsive
- 🎨 Rich embeds for song information
- 🔗 Support for direct YouTube URLs
- ❌ Cancellable song selection

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
  - Accepts YouTube URLs directly
  - Provides interactive search results for song names
  - Shows song thumbnails and details
- `/sync` - Sync slash commands with Discord
- `/test` - Test command to verify bot functionality

### Example Usage
```
/play Bohemian Rhapsody
/play https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

## Dependencies

Main dependencies:
- discord.py - Discord API wrapper
- python-dotenv - Environment variable management
- pytubefix - YouTube video processing
- validators - URL validation
- requests - HTTP requests
- aiohttp - Async HTTP client
- aiohappyeyeballs - Network connection optimization

For a complete list of dependencies and their versions, see `requirements.txt`.

## Configuration

The bot uses environment variables for configuration:
- `DISCORD_TOKEN`: Your Discord bot token
- `SYMBOL`: The command prefix for traditional commands
- `API_HOST`: The host address for the karaoke API server

## Features in Detail

### Song Search
When users search for a song without providing a URL, the bot:
1. Searches YouTube for the top 10 matching results
2. Displays an interactive selection menu
3. Shows song thumbnails and titles
4. Allows users to cancel their selection
5. Provides visual feedback for selected songs

### URL Processing
When users provide a direct YouTube URL, the bot:
1. Validates the URL format
2. Extracts video information
3. Queues the song directly
4. Displays song details in an embed

### Rich Embeds
All bot responses use Discord embeds featuring:
- Song thumbnails
- Requester information
- Timestamps
- Color coding for different message types
- Interactive components where applicable