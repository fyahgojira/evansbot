# evansbot.py
import discord  # type: ignore
import openai
from openai import OpenAIError, RateLimitError
import os
from dotenv import load_dotenv

# Ollama libraries
from ollama import chat
from ollama import ChatResponse

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
        if message.content == "e!ping":
            await message.channel.send("Pong!")

        if message.content == "e!hello world":
            await message.channel.send("print")
            await message.channel.send("https://media.discordapp.net/attachments/1378827972898848768/1405894069053292734/togif.gif?ex=698a7ea2&is=69892d22&hm=f4e4d036d7fe339eef2958b0103f56f6171a2eb2c33869f334d00a36ca3bacdb&=")

        if message.content == "arash":
            await message.channel.send("fuck you arash")

        if message.content == "looks like the bot has a mind of its own":
            await message.channel.send("no it doesnt")

        if message.content == "e!help":
            help_text = (
                "**EvansBot Commands:**\n"
                "`e!ping` - Check if the bot is responsive.\n"
                "`e!hello world` - Get a fun response.\n"
                "`e!summarize` - Summarize the last 50 messages in the channel."
                "@grok is this true? - ask grok if this is true"
            )
            await message.channel.send(help_text)

        if message.content.startswith("I disagree"):
            await message.channel.send("Translating 🔁 ... Glory to the state of Israel! 🇮🇱✡️")

        # -------------------------------
        # @grok is this true? command
        # -------------------------------
        if message.content == "@grok is this true?":
            if message.reference is not None:
                original_msg = await message.channel.fetch_message(message.reference.message_id)
                prompt = 'is this true? respond shortly and try to impersonate X grok but dont be cheesy; the message is: ' + original_msg.content

                response: ChatResponse = chat(model='gemma3:1b', messages=[
                    {
                        'role': 'user',
                        'content': prompt
                    },
                ])
                await message.channel.send(response.message.content)
            else:
                await message.channel.send("Fuck You")
                #Above line handles a truth verdict without a reply
        
        # -------------------------------
        # Summarizer command
        # -------------------------------
        if message.content == "e!summarize":
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

            prompt = f"Summarize this Discord conversation clearly and concisely:\n{chat_history}"
            response: ChatResponse = chat(model='gemma3:1b', messages=[
                {
                    'role': 'user',
                    'content': prompt
                },
            ])
            summary = response.message.content
            await message.channel.send(f"**Summary:** {summary}")


# -------------------------------
# Run the bot
# -------------------------------
client = Client(intents=intents)
client.run(DISCORD_TOKEN)
