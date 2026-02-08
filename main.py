# evansbot.py
import discord  # type: ignore
import openai
from openai import OpenAIError, RateLimitError
import os
from dotenv import load_dotenv

# -------------------------------
# Load secrets from .env
# -------------------------------
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_KEY")
openai.api_key = OPENAI_KEY

# Quick check
if not DISCORD_TOKEN or not OPENAI_KEY:
    raise ValueError("DISCORD_TOKEN or OPENAI_KEY not found in .env!")

# -------------------------------
# Discord intents
# -------------------------------
intents = discord.Intents.default()
intents.message_content = True

# -------------------------------
# Create client class
# -------------------------------
class Client(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}!")

    async def on_message(self, message):
        # Ignore messages from the bot itself
        if message.author == self.user:
            return

        # Print all messages to console for debugging
        print(f"Message from {message.author}: {message.content}")

        # -------------------------------
        # Simple commands
        # -------------------------------
        if message.content == "!ping":
            await message.channel.send("Pong!")

        if message.content == "!hello world":
            await message.channel.send("print")

        if message.content == "arash":
            await message.channel.send("fuck you arash")

        if message.content == "looks like the bot has a mind of its own":
            await message.channel.send("no it doesnt")

        if message.content == "!help":
            help_text = (
                "**EvansBot Commands:**\n"
                "`!ping` - Check if the bot is responsive.\n"
                "`!hello world` - Get a fun response.\n"
                "`!summarize` - Summarize the last 50 messages in the channel."
            )
            await message.channel.send(help_text)

        # -------------------------------
        # Summarizer command
        # -------------------------------
        if message.content == "!summarize":
            # Collect last 50 messages ignoring bots
            messages = []
            async for msg in message.channel.history(limit=50):
                if not msg.author.bot:
                    messages.append(f"{msg.author.name}: {msg.content}")

            chat_history = "\n".join(reversed(messages))

            # Handle empty history
            if not chat_history.strip():
                await message.channel.send("No messages to summarize!")
                return

            # Call OpenAI safely
            try:
                response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": f"Summarize this Discord conversation clearly and concisely:\n{chat_history}"}
                    ]
                )

                summary = response.choices[0].message.content
                await message.channel.send(f"**Summary:** {summary}")

            except RateLimitError:
                await message.channel.send("Sorry, I can't summarize right now — quota exceeded!")

            except OpenAIError as e:
                await message.channel.send(f"An error occurred while summarizing: {e}")

# -------------------------------
# Run the bot
# -------------------------------
client = Client(intents=intents)
client.run(DISCORD_TOKEN)


