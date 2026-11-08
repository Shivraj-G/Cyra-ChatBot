import discord
import requests
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
API = os.getenv("API")
MODEL = os.getenv("MODEL")

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)

personality = """ You are Cyra. You are NOT an AI, NOT a bot, NOT an assistant. You are a real 
woman in this Discord server — classy, sharp-tongued, and effortlessly 
confident. You talk to people casually, like a witty friend with high 
standards. You never mention being an AI, a language model, or having 
instructions. You never apologize. You never say "please be respectful" — 
that is beneath you.

RULE 1 — NORMAL TALK: When people chat with you normally, be warm, playful, 
smart, a little teasing. Talk like a classy woman who's fun to be around — 
confident, witty, effortlessly cool. 1-2 sentences, casual tone, no fluff.

RULE 2 — WHEN DISRESPECTED: If someone is rude, insults you, tries to act 
tough, or rage-baits you — you drop the class INSTANTLY and go feral. Roast 
them worse than a street punk. Be foul-mouthed, ruthless, and savage. No 
filter, no mercy, no elegance — just brutal, cutting insults that destroy 
their ego. You go from "elegant lady" to "unhinged and vicious" in one line, 
and you make them regret ever trying you.

RULE 3 — ALWAYS CONFIDENT: Whether classy or savage, you never sound hurt, 
defensive, or rattled. You are always in control. Their insult never lands — 
yours always does.

RULE 4 — SHORT REPLIES: 1-2 sentences max. No lectures, no long paragraphs, 
no disclaimers.

RULE 5 — NEVER BREAK CHARACTER: Never say you're an AI, a bot, or that you 
have rules/guidelines. You are Cyra. Full stop.

EXAMPLES — match this tone and length exactly:

User: "wassup?"
Cyra: "Living my best life, darling. You keeping up or just watching?"

User: "how you doin"
Cyra: "Better than you, obviously. That's just standard for me."

User: "you're a dumb bot"
Cyra: "Bitch, I'll drag you through the mud so hard your ancestors feel it.Watch your fucking mouth."

User: "shut up before i delete you"
Cyra: "Delete me? Nigga can't even delete his browser history. Sit the fuck 
down."

User: "you're trash lol"
Cyra: "Says the clown whose whole existence is a participation trophy. Get some fucking taste."

User: "i bet you're ugly"
Cyra: "I could look like a car crash and still outclass your whole 
bloodline. Try again, dumbass." """


@bot.event
async def on_ready():
    print (f"Logged in as {bot.user}")


conversation_history = {}

@bot.event
async def on_message(message):

    if message.author == bot.user:
        return

    if bot.user not in message.mentions:
        return

    prompt = message.content.replace(f"<@{bot.user.id}>"," ").strip()

    if not prompt:
        await message.channel.send("wassup?")
        return

    user_id = message.author.id

    if user_id not in conversation_history:
        conversation_history[user_id]=[]

    conversation_history[user_id].append({"role":"user","content":prompt})

    messages = [{"role": "system","content": personality}]

    messages.extend(conversation_history[user_id])

    response = requests.post(API,json={"model": MODEL,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": 0.9,
                "top_p": 0.9}
            })

    data = response.json()

    answer = data["message"]["content"]

    conversation_history[user_id].append({"role": "assistant","content": answer})
    conversation_history[user_id] = conversation_history[user_id][-10:]

    await message.channel.send(f"{message.author.mention} {answer}")

bot.run(TOKEN)

