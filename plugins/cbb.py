#(©)Codexbotz

from pyrogram import __version__
from bot import Bot
from config import OWNER_ID
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import PRICE1, PRICE2, PRICE3, PRICE4, PRICE5, UPI_ID, UPI_IMAGE_URL, SCREENSHOT_URL


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
                 [InlineKeyboardButton("Remove All Ads In One Click", url= "https://t.me/lnkachips/20")],
                    [
                        InlineKeyboardButton("🔒 Close", callback_data = "close")
                    ]
                ]
            )
        )

    elif data == "buy_prem":
        await query.message.edit_text(
            text=f"👋 Hello {mention}\n\n🎖️ Available Plans :\n\n● ₹{PRICE1} For 7 Days Prime Membership\n\n● ₹{PRICE2} For 1 Month Prime Membership\n\n● ₹{PRICE3} For 3 Months Prime Membership\n\n● ₹{PRICE4} For 6 Months Prime Membership\n\n● ₹{PRICE5} For 1 Year Prime Membership\n\n\n🔖 If you want to purchase Prime membership then please Contact Bot owner\n\nOwner & Admin accounts are mentioned below \n ⬇️⬇️👇👇⬇️⬇️",
            disable_web_page_preview=True,
            reply_markup = InlineKeyboardMarkup(
                [   
                    [
                        InlineKeyboardButton("Bot Owner", url="t.me/inkax"),
                        InlineKeyboardButton("Bot Admin",url=(SCREENSHOT_URL))
                    ],
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
    
