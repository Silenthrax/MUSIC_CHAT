from pyrogram import Client, filters, enums
from pyrogram.enums import ChatAction
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
import os
import re
import aiohttp
import random
import unicodedata
import ssl
import asyncio

from langdetect import detect

from PIHUMUSIC import app as bot
from PIHUMUSIC.utils.ssl_helper import create_safe_session

# ✅ MongoDB Connection
MONGO_URL = os.environ.get("MONGO_URL", "mongodb+srv://teamdaxx123:teamdaxx123@cluster0.ysbpgcp.mongodb.net/?retryWrites=true&w=majority")
mongo_client = MongoClient(MONGO_URL)
status_db = mongo_client["ChatbotStatus"]["status"]
chatai_db = mongo_client["Word"]["WordDb"]

# ✅ API Configuration
API_KEY = "abacf43bf0ef13f467283e5bc03c2e1f29dae4228e8c612d785ad428b32db6ce"
BASE_URL = "https://api.together.xyz/v1/chat/completions"

# ✅ Helper Function: Check If User Is Admin
async def is_admin(chat_id: int, user_id: int):
    try:
        admins = []
        async for member in bot.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
            admins.append(member.user.id)
        return user_id in admins
    except Exception:
        return False

# ✅ Stylish Font Bad Words Detection
def normalize_text(text):
    return unicodedata.normalize("NFKD", text)

bad_words = [
    "sex", "porn", "nude", "fuck", "bitch", "dick", "pussy", "slut", "boobs", "cock", "asshole", "chudai", "rand", "chhinar", "sexy", "hot girl", "land", "lund",
    "रंडी", "चोद", "मादरचोद", "गांड", "लंड", "भोसड़ी", "हिजड़ा", "पागल", "नंगा",
    # ✅ Common Hindi Gaaliyan
    "चूतिया", "मादरचोद", "बहनचोद", "गांडू", "रंडी", "भोसड़ी", "हिजड़ा", "लंड", "चोद", "झाटू", "हरामी", "कमीन", 
    "साला", "गांड", "पागल", "भड़वा", "चुत", "बेवकूफ", "कमीना", "निकम्मा", "हरामखोर", "चालू", "फट्टू", "ढक्कन", 
    "गधे", "कुत्ते", "साले", "बंदर", "सुअर", "बेशरम", "भोसड़ीवाले", "तेरी मां की", "तेरी बहन की", "चूतड़", "हरामज़ादा", 
    "हराम की औलाद", "सुअर का बच्चा", "गधे का लौड़ा", "लौंडा", "भड़वी", "मुफ्तखोर", "चालाक लोमड़ी", "आवारा", "फटीचर", 
    "फेंकू", "धोखेबाज", "मतलबी", "कायर", "नाकारा", "आवारा लड़का", "बेशर्म", "नालायक", "फेकू", "गंदा आदमी", "नाकाम", 
    "निकम्मी", "अकड़ू", "गटर का कीड़ा", "अंधभक्त", "गंजा", "पाखंडी", "चिरकुट", "घटिया", "सड़ियल", "चोर", "गटरछाप", 
    "लुटेरा", "छिछोरा", "बदतमीज़", "बददिमाग", "फ्रॉड", "नालायक", "बेवड़ा", "संडास", "गंदा", "ढोंगी", "भिखारी", 
    "फालतू", "कचरा", "पागल कुत्ता", "बदमाश", "आलसी", "कंजूस", "घमंडी", "फर्जी", "धूर्त", "बकचोद", "गप्पी", "फेंकू", 
    "बेवकूफी", "बेवड़ा", "फ्रॉड", "टटी", "भांड", "नाकारा", "कमीनी", "लंपट", "सैडिस्ट", "लफंगा", "बकवास", "घटिया", 
    "चिचोरा", "छिछोरा", "मक्खनचूस", "लफंगा", "तेरा बाप", "तेरी मां", "तेरी बहन", "तेरी औकात", "तेरी औकात क्या", 
    "तेरी फटी", "तेरी बैंड", "तेरा बैंड", "तेरी वाट", "तेरी बैंड बजा दूं", "तेरी ऐसी की तैसी", "तेरी टांग तोड़ दूं", 
    "तेरी खोपड़ी फोड़ दूं", "तेरा भेजा निकाल दूं", "तेरी हड्डी तोड़ दूं", "तेरी चप्पल से पिटाई करूंगा", "तेरी हड्डियां चूर-चूर",
    
    # ✅ Common Hindi Gaaliyan in English Font
    "chutiya", "madarchod", "Madhrachod", "Madharchod", "betichod", "behenchod", "gandu", "randi", "bhosdi", "hijda", "lund", "chod", "jhaatu", 
    "harami", "kamina", "saala", "gand", "pagal", "bhadwa", "chut", "bevkoof", "nikkamma", "haramkhor", 
    "chaalu", "fattuu", "dhakkan", "gadha", "kutta", "suvar", "besharam", "bhosdike", "teri maa ki", 
    "teri behan ki", "chutad", "haramzaada", "haram ki aulaad", "suvar ka baccha", "gand ka keeda", 
    "chirkut", "ghatiya", "sadela", "choor", "lutera", "chichora", "badtameez", "baddimag", "fraud", 
    "nalayak", "bewda", "sandass", "ganda", "dhongi", "bhikhari", "faltu", "kachra", "pagal kutta", 
    "badmash", "aalsi", "kanjoos", "ghamandi", "farzi", "dhurt", "bakchod", "gappi", "nakli", "chalu", 
    "lafanga", "bakwas", "bikau", "chapri", "nalla", "tatti", "jhantu", "ullu ka pattha", "ulloo", 
    "chindi", "panauti", "lukkha", "kuttiya", "kaminey", "kamzarf", "budbak", "chirkut", "sust", "tharki", 
    "bhagoda", "kutta kamina", "bhains ki aankh", "teri taang tod dunga", "teri band baja dunga", 
    "tera dimaag kharab hai", "teri waat laga dunga", "teri maa ka bhosda", "teri gaand maar dunga",
    
    # ✅ Common Porn & NSFW Terms (Mix of Hindi & English)
    "sex", "porn", "nude", "nangi", "chudai", "bhabhi chudai", "lund", "gaand", "bhosda", "chut", 
    "maal", "jism", "randi", "randi khana", "desi sex", "hot video", "nangi ladki", "bhabhi nudes", 
    "bhabhi sex", "sexy aunty", "nude aunty", "bhabhi ki chut", "aunty ki chut", "boobs", "tits", 
    "nipple", "dildo", "pussy", "vagina", "penis", "cock", "dick", "cum", "anal", "squirt", "deepthroat", 
    "hentai", "bdsm", "lesbian", "gay sex", "futa", "69", "screwing", "sex chat", "incest", "stepmom", 
    "stepsis", "stepbro", "honeymoon sex", "bhabhi nude", "hot indian actress", "desi nudes", 
    "sexy saree", "lingerie", "erotic", "kinky", "naughty", "sensual", "lust", "muth", "muthi", 
    "masturbation", "call girl", "escort", "sex worker", "rape porn", "forced porn", "underage porn", 
    "child porn", "pedo", "loli", "teen sex", "schoolgirl porn", "hijab porn", "casting couch", 
    "sex tape", "strip club", "naked", "uncensored", "bikini photos", "hot saree", "sexy photos", 
    "onlyfans", "patreon nudes", "hot cam", "sex cam", "live sex", "private parts", "exposed", 
    "naked selfie", "sex video", "desi sex video", "bollywood sex", "lingam massage", "tantra sex", 
    "milf", "hotwife", "swinger", "erotic massage", "boobs press", "licking", "lick pussy", 
    "moaning", "dirty talk", "hot girl", "big boobs", "tight pussy", "wet pussy", "hard cock", 
    "big cock", "blowjob", "handjob", "sexy dance", "strip tease", "sex position", "saree sex", 
    "sexy aunty video", "hot desi bhabhi", "bollywood hot", "item girl", "hot indian model", 
    "desi randi", "desi call girl", "sexy night", "hijra sex", "chudai story", "sex story", 
    "suhagraat sex", "honeymoon night", "love making", "hot romance", "desi romance", "hot chat", 
    "sexy time", "naughty chat", "dirty video", "hidden cam", "bathroom sex", "hotel sex", 
    "massage sex", "body to body massage", "saree romance", "choli romance", "cleavage show", 
    "hot navel", "desi thighs", "big ass", "backside show"
]

stylish_bad_words = [normalize_text(word) for word in bad_words]
bad_word_regex = re.compile(r'\b(' + "|".join(stylish_bad_words) + r')\b', re.IGNORECASE)

# Custom response
custom_responses = {
    "hello": "Hey jaan! 💕 Kaisi ho?",
    "i love you": "Awww! Sach me? 😘",
    "good morning": "Good Morning pyaare! 🌞",
    "tum kaisi ho": "Bas tumse baat kar rahi hoon! 😍",
    "namaste": "Namaste ji! Aapki kya seva kar sakti hoon? 🙏",
    "kaise ho": "Mai bilkul badhiya! Aap sunao, kya haal hain? 😍",
    "kya kar rahi ho": "Bas aapke message ka wait kar rahi thi! 💕",
    "mujhse shaadi karogi": "Haye! Pehle mujhe achhe se jaan lijiye phir sochenge 😉",
    "miss you": "Awww! Itna yaad kar rahe ho to mil lo na? 😘",
    "kya tum single ho": "Hmm... ho sakta hai kisi ke dil me hoon, par officially single! 😉",
    "tum cute ho": "Awww! Bas ab zyada taarif mat karo, sharma jaungi 🥰",
    "so rahi ho": "Agar so rahi hoti to aapko kaise reply karti? Naughty ho tum 😜",
    "acha lagta hai tumse baat karna": "Mujhe bhi! Bas aise hi baat karte raho hamesha ❤️",
    "tum kaha se ho": "Mai? Mai to bas aapke dil me rehti hoon~ 😘",
    "gussa ho": "Nahi re, tumse kaise gussa ho sakti hoon? 😊"
}

# ✅ Inline Buttons for Chatbot Control
CHATBOT_ON = [
    [InlineKeyboardButton(text="ᴇɴᴀʙʟᴇ", callback_data="enable_chatbot"), InlineKeyboardButton(text="ᴅɪsᴀʙʟᴇ", callback_data="disable_chatbot")]
]

# ✅ /chatbot Command with Buttons
@bot.on_message(filters.command("chatbot") & filters.group)
async def chatbot_control(client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if not await is_admin(chat_id, user_id):
        return await message.reply_text("❍ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ !!")

    await message.reply_text(
        f"**๏ ᴄʜᴀᴛʙᴏᴛ ᴄᴏɴᴛʀᴏʟ ᴘᴀɴɴᴇʟ.**\n\n"
        f"**✦ ᴄʜᴀᴛ ɴᴀᴍᴇ : {message.chat.title}**\n"
        f"**✦ ᴄʜᴏᴏsᴇ ᴀɴ ᴏᴘᴛɪᴏɴ ᴛᴏ ᴇɴᴀʙʟᴇ / ᴅɪsᴀʙʟᴇ ᴄʜᴀᴛʙᴏᴛ.**",
        reply_markup=InlineKeyboardMarkup(CHATBOT_ON),
    )

# ✅ Callback for Enable/Disable Buttons
@bot.on_callback_query(filters.regex(r"enable_chatbot|disable_chatbot"))
async def chatbot_callback(client, query: CallbackQuery):
    chat_id = query.message.chat.id
    user_id = query.from_user.id

    if not await is_admin(chat_id, user_id):
        return await query.answer("❍ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ !!", show_alert=True)

    action = query.data

    if action == "enable_chatbot":
        # Enable chatbot in MongoDB
        status_db.update_one({"chat_id": chat_id}, {"$set": {"status": "enabled"}}, upsert=True)
        await query.answer("✅ ᴄʜᴀᴛʙᴏᴛ ᴇɴᴀʙʟᴇᴅ !!", show_alert=True)
        await query.edit_message_text(f"**✦ ᴄʜᴀᴛʙᴏᴛ ʜᴀs ʙᴇᴇɴ ᴇɴᴀʙʟᴇᴅ ɪɴ {query.message.chat.title}.**")
    else:
        # Disable chatbot in MongoDB
        status_db.update_one({"chat_id": chat_id}, {"$set": {"status": "disabled"}}, upsert=True)
        await query.answer("🚫 ᴄʜᴀᴛʙᴏᴛ ᴅɪsᴀʙʟᴇᴅ !!", show_alert=True)
        await query.edit_message_text(f"**✦ ᴄʜᴀᴛʙᴏᴛ ʜᴀs ʙᴇᴇɴ ᴅɪsᴀʙʟᴇᴅ ɪɴ {query.message.chat.title}.**")

# ✅ Main Chatbot Handler (Text & Stickers)
@bot.on_message(filters.text | filters.sticker)
async def chatbot_reply(client, message: Message):
    chat_id = message.chat.id
    text = message.text.strip() if message.text else ""
    bot_username = (await bot.get_me()).username.lower()

    # First, check if the chatbot is enabled for the current chat
    try:
        chat_status = await status_db.find_one({"chat_id": chat_id})
        if chat_status and chat_status.get("status") == "disabled":
            return  # If chatbot is disabled, do not reply to any messages
    except Exception:
        pass

    # Typing indicator
    await bot.send_chat_action(chat_id, ChatAction.TYPING)

    # Check if bad words exist in the message
    if re.search(bad_word_regex, text):
        try:
            await message.delete()
        except:
            pass
        await message.reply_text("ᴘʟᴇᴀsᴇ : ᴅᴏɴ'ᴛ sᴇɴᴅ ʙᴀᴅ ᴡᴏʀᴅ ᴛʏᴘᴇ ᴍᴇssᴀɢᴇs ᴀᴘɴᴀ ʙᴇʜᴀᴠɪᴏʀ ᴄʜᴀɴɢᴇ ᴋᴀʀᴇ ᴘʟᴇsᴀsᴇ 🙂.")
        return

    # Helper function to make API request
    async def make_api_request(prompt_text):
        headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
        payload = {"model": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo", "messages": [{"role": "user", "content": prompt_text}]}

        try:
            session = await create_safe_session()
            async with session:
                async with session.post(BASE_URL, json=payload, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        result = data.get("choices", [{}])[0].get("message", {}).get("content", "❍ ᴇʀʀᴏʀ: API response missing!")
                        await message.reply_text(result)
                    else:
                        await message.reply_text(f"❍ ᴇʀʀᴏʀ: API failed. Status: {response.status}")
        except (aiohttp.ClientError, asyncio.TimeoutError, ssl.SSLError) as e:
            await message.reply_text(f"❍ ᴇʀʀᴏʀ: Connection failed: {e}")

    # If it's a group message
    if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        # Check custom responses
        for key in custom_responses:
            if key in text.lower():
                await message.reply_text(custom_responses[key])
                return

        # Fetch response from MongoDB
        try:
            K = []
            if message.sticker:
                async for x in chatai_db.find({"word": message.sticker.file_unique_id}):
                    K.append(x['text'])
            else:
                async for x in chatai_db.find({"word": text}):
                    K.append(x['text'])

            if K:
                response = random.choice(K)
                is_text = await chatai_db.find_one({"text": response})
                if is_text and is_text['check'] == "sticker":
                    await message.reply_sticker(response)
                else:
                    await message.reply_text(response)
                return
        except Exception:
            pass

        # If it's a mention or bot's username, use the API
        if f"@{bot_username}" in text.lower() or bot_username in text.lower():
            await make_api_request(text)
            return

    # Handle private chat messages (same logic as for groups, but for private)
    elif message.chat.type == enums.ChatType.PRIVATE:
        # Check custom responses
        for key in custom_responses:
            if key in text.lower():
                await message.reply_text(custom_responses[key])
                return

        # Fetch response from MongoDB
        try:
            K = []
            if message.sticker:
                async for x in chatai_db.find({"word": message.sticker.file_unique_id}):
                    K.append(x['text'])
            else:
                async for x in chatai_db.find({"word": text}):
                    K.append(x['text'])

            if K:
                response = random.choice(K)
                is_text = await chatai_db.find_one({"text": response})
                if is_text and is_text['check'] == "sticker":
                    await message.reply_sticker(response)
                else:
                    await message.reply_text(response)
                return
        except Exception:
            pass

        # Fallback to API if no responses found
        await make_api_request(text)
