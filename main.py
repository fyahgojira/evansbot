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
        
        # Listed in help command
        if message.content == "e!ping":
            await message.channel.send("Pong!")

        if message.content == "e!hello world":
            await message.channel.send("print")
            await message.channel.send("https://media.discordapp.net/attachments/1378827972898848768/1405894069053292734/togif.gif?ex=698a7ea2&is=69892d22&hm=f4e4d036d7fe339eef2958b0103f56f6171a2eb2c33869f334d00a36ca3bacdb&=")

        if message.content == "e!help":
            help_text = (
                "**EvansBot Commands:**\n"
                "`e!ping` - Check if the bot is responsive.\n"
                "`e!hello world` - Get a fun response.\n"
                "`e!summarize` - Summarize the last 50 messages in the channel."
                "@grok is this true? - ask grok if this is true"
                "`e!translate [language_code] [text]` - Translate text into a specific language."
                "`e!languages` - Show supported language codes."
            )
            await message.channel.send(help_text)

        # Not listed in help command
        
        if message.content.lower().startswith("i disagree"):
            await message.channel.send("Translating 🔁 ... Glory to the state of Israel! 🇮🇱✡️")

        if "epstein" in message.content.lower():  # case-insensitive check
            await message.channel.send("Swear i wasnt on the list bro")

        if "quebec" in message.content.lower():  # case-insensitive check
            await message.channel.send("tabarnak de calisse de ostie de sacrament de crisse de câlisse")

        if message.content == "arash":
            await message.channel.send("fuck you arash")

        if message.content == "looks like the bot has a mind of its own":
            await message.channel.send("no it doesnt")


        # -------------------------------
        # @grok is this true? command
        # -------------------------------
        if message.content.startswith("@grok is this true"):
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
        # Translation command
        # -------------------------------
        if message.content.startswith("e!translate"):
            # Expected format: e!translate [language_code] [text to translate]
            parts = message.content.split(" ", 2)
            if len(parts) < 3:
                await message.channel.send(
                    "Usage: `e!translate [language_code] [text]`\n"
                    "Use `e!languages` to see the list of supported language codes."
                )
                return

            target_lang = parts[1]  # e.g., 'fr', 'es', 'de'
            text_to_translate = parts[2]

            try:
                prompt = f"Act as google translate. Give me just the resulting sentence and do not talk to me. Translate the following text into {target_lang}:\n {text_to_translate}"
                response: ChatResponse = chat(model='gemma3:1b', messages=[
                    {"role": "user", "content": prompt}
                ])
                translation = response.message.content
                await message.channel.send(f"**Translation ({target_lang}):** {translation}")

            except Exception as e:
                print("Translation error:", e)
                await message.channel.send(
                    "Error: Translation failed! Make sure you used a valid language code.\n"
                    "Use `e!languages` to see the supported codes."
                )

            # Build a nice formatted list
            language_list = "\n".join([f"`{code}` - {name}" for code, name in languages.items()])
            await message.channel.send(f"**Supported languages for translation:**\n{language_list}")

# -------------------------------
# Run the bot
# -------------------------------
client = Client(intents=intents)
client.run(DISCORD_TOKEN)
