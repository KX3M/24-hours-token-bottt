```python
# (Ã‚Â©)CodeXBotz
import asyncio
import base64
import logging
import os
import random
import re
import string
import time

from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from bot import Bot
from config import (
    ADMINS,
    FORCE_MSG,
    START_MSG,
    CUSTOM_CAPTION,
    IS_VERIFY,
    VERIFY_EXPIRE,
    SHORTLINK_API,
    SHORTLINK_URL,
    DISABLE_CHANNEL_BUTTON,
    PROTECT_CONTENT,
    TUT_VID,
    OWNER_ID,
)
from helper_func import subscribed, encode, decode, get_messages, get_shortlink, get_verify_status, update_verify_status, get_exp_time
from database.database import add_user, del_user, full_userbase, present_user
from shortzy import Shortzy

"""Add time in seconds for waiting before delete
1min=60, 2min=60×2=120, 5min=60×5=300"""
SECONDS = int(os.getenv("SECONDS", "300"))

@Bot.on_message(filters.command('start') & filters.private & subscribed)
async def start_command(client: Client, message: Message):
    id = message.from_user.id
    owner_id = OWNER_ID  # Fetch the owner's ID from config

    # Check if the user is the owner
    if id == owner_id:
        # Owner-specific actions
        await message.reply("You are the owner! Additional actions can be added here.")
    else:
        if not await present_user(id):
            try:
                await add_user(id)
            except:
                pass

        verify_status = await get_verify_status(id)
        if verify_status['is_verified'] and VERIFY_EXPIRE < (time.time() - verify_status['verified_time']):
            await update_verify_status(id, is_verified=False)

        if "verify_" in message.text:
            _, token = message.text.split("_", 1)
            if verify_status['verify_token'] != token:
                return await message.reply("Your token is invalid or expired. Try again by clicking /start")
            await update_verify_status(id, is_verified=True, verified_time=time.time())
            reply_markup = None
            await message.reply(f"Your token successfully verified and valid for: 24 hours", reply_markup=reply_markup, protect_content=True, quote=True)
        
        elif len(message.text) > 7 and verify_status['is_verified']:
            try:
                base64_string = message.text.split(" ", 1)[1]
            except:
                return
            _string = await decode(base64_string)
            argument = _string.split("-")
            if len(argument) == 3:
                try:
                    start = int(int(argument[1]) / abs(client.db_channel.id))
                    end = int(int(argument[2]) / abs(client.db_channel.id))
                except:
                    return
                ids = range(start, end+1) if start <= end else list(range(start, end-1, -1))
            elif len(argument) == 2:
                try:
                    ids = [int(int(argument[1]) / abs(client.db_channel.id))]
                except:
                    return
            else:
                ids = []

            temp_msg = await message.reply("Please wait...")
            try:
                messages = await get_messages(client, ids)
            except:
                await message.reply_text("Something went wrong..!")
                return
            await temp_msg.delete()

            for msg in messages:
                caption = (CUSTOM_CAPTION.format(previouscaption=msg.caption.html if msg.caption else "", filename=msg.document.file_name)
                           if CUSTOM_CAPTION and msg.document else msg.caption.html if msg.caption else "")
                reply_markup = msg.reply_markup if DISABLE_CHANNEL_BUTTON else None

                try:
                    await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                    await asyncio.sleep(0.5)
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                except:
                    pass

            k = await message.reply_text("<b>â—ï¸ <u>baka!</u> â—ï¸</b>\n\n<b>This video/file will be deleted in 10 minutes (due to copyright issues).\n\nðŸ“Œ Please forward this video/file to somewhere else and start downloading there.</b>")
            await asyncio.sleep(SECONDS)

            for data in messages:
                try:
                    await data.delete()
                    await k.edit_text("<b>Your video/file is successfully deleted!</b>")
                except:
                    pass
        
        elif verify_status['is_verified']:
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Main Channel", url="t.me/InkaLinks"),
                        InlineKeyboardButton("Source Code", url="https://t.me/+nrNgQ7sT3XQxZTc1")
                    ],
                    [InlineKeyboardButton("Remove All Ads In One Click", callback_data="buy_prem")],
                    [
                        InlineKeyboardButton("ðŸ¤– About Me", callback_data="about"),
                        InlineKeyboardButton("ðŸ”’ Close", callback_data="close")
                    ]
                ]
            )
            await message.reply_text(
                text=START_MSG.format(
                    first=message.from_user.first_name,
                    last=message.from_user.last_name,
                    username=None if not message.from_user.username else '@' + message.from_user.username,
                    mention=message.from_user.mention,
                    id=message.from_user.id
                ),
                reply_markup=reply_markup,
                disable_web_page_preview=True,
                quote=True
            )
        else:
            verify_status = await get_verify_status(id)
            if IS_VERIFY and not verify_status['is_verified']:
                short_url = f"api.publicearn.com"
                full_tut_url = f"https://t.me/sotutorials/6"
                token = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
                await update_verify_status(id, verify_token=token, link="")
                link = await get_shortlink(SHORTLINK_URL, SHORTLINK_API, f'https://telegram.dog/{client.username}?start=verify_{token}')
                btn = [
                    [InlineKeyboardButton("Click Here To Refresh Token", url=link)],
                    [InlineKeyboardButton('How To Use The Bot', url=full_tut_url)],
                    [InlineKeyboardButton("Remove All Ads In One Click", callback_data="buy_prem")]
                ]
                await message.reply(f"Your ads token is expired, refresh your token and try again.\n\nToken Timeout: {get_exp_time(VERIFY_EXPIRE)}\n\n<b>What is the token?</b>\n\nThis is an ads token. If you pass 1 ad, you can use the bot for 24 hours after passing the ad.", reply_markup=InlineKeyboardMarkup(btn), protect_content=False, quote=True)

# ... (rest of the code remains unchanged)

WAIT_MSG = """<b>Processing ...</b>"""

REPLY_ERROR = """<code>Use this command as a reply to any telegram message without any spaces.</code>"""

@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    buttons = [
        [
            InlineKeyboardButton("Join Channel", url=client.invitelink),
            InlineKeyboardButton("Join Channel", url="https://t.me/+wyYRizWWncNmMmJk")
        ]
    ]
    try:
        buttons.append(
            [
                InlineKeyboardButton(
                    text='â™»ï¸ Try Again â™»ï¸',
                    url=f"https://t.me/{client.username}?start={message.command[1]}"
                )
            ]
        )
    except IndexError:
        pass

    await message.reply(
        text=FORCE_MSG.format(
            first=message.from_user.first_name,
            last=message.from_user.last_name,
            username=None if not message.from_user.username else '@' + message.from_user.username,
            mention=message.from_user.mention,
            id=message.from_user.id
        ),
        reply_markup=InlineKeyboardMarkup(buttons),
        quote=True,
        disable_web_page_preview=True
    )

@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await full_userbase()
    await msg.edit(f"{len(users)} users are using this bot")

@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0
        
        pls_wait = await message.reply("<i>Broadcasting message.. This will take some time</i>")
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await del_user(chat_id)
                blocked += 1
