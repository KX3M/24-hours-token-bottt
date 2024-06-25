#(©)Codexbotz

from pyrogram import __version__
from bot import Bot
from config import OWNER_ID
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    if data == "about":
        await query.message.edit_text(
            text = f"<b>👨‍💻 𝘋𝘦𝘷𝘭𝘰𝘱𝘦𝘳 :</b> <a href='https://t.me/ifeelscam'>sʜᴀɪᴋʜ ᴀʟɪ</a> \n<b> 🤖 𝘊𝘳𝘦𝘢𝘵𝘰𝘳 :</b> <a href='t.me/InkaLinks'> ᴄʜɪᴘs</a></b>",
            disable_web_page_preview = True,
            reply_markup = InlineKeyboardMarkup(
                [ [ InlineKeyboardButton(" Source code ", url="https://t.me/+NeqCUg-QDxo2Nzll"),
                  InlineKeyboardButton("Bot Channel" , url= "https://t.me/publicfille")],
                    [
                        InlineKeyboardButton("🔒 Close", callback_data = "close")
                    ]
                ]
            )
        )
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except: 
            pass
   elif data == "buy_y":
        await query.message.edit_text(
            text=f"👋 {query.from_user.username}\n\n🎖️ Available Plans :\n\n● 40 rs For 7 Days Prime Membership\n\n● 140 rs For 1 Month Prime Membership\n\n● 400 rs For 3 Months Prime Membership\n\n● 750 rs For 6 Months Prime Membership\n\n● 1200 rs For 1 Year Prime Membership\n\n\n💵 UPI ID -  deal@psb\n\n(Tap to copy UPI Id)\n\n\n📸 QR - ᴄʟɪᴄᴋ ʜᴇʀᴇ ᴛᴏ ꜱᴄᴀɴ (https://graph.org/file/a95389977b7ca92016eb4.jpg)\n\n♻️ If payment is not getting sent on above given QR code then inform admin, he will give you new QR code\n\n\n‼️ Must Send Screenshot after payment",
            disable_web_page_preview=True,
            reply_markup = InlineKeyboardMarkup(
                [   
                    [
                        InlineKeyboardButton("Send Payment Screenshot(ADMIN) 📸", url= "t.me/lnkaChipsbot")
                    ],
                    [
                        InlineKeyboardButton("🔒 Close", callback_data = "close")
                    ]
                ]
            )
    )
