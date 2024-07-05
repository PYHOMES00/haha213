from plugins.forcesub import ForceSub
import os
import sys
import asyncio 
from database import db, mongodb_version
from config import Config, temp
from platform import python_version
from translation import Translation
from pyrogram import Client, filters, enums, __version__ as pyrogram_version
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaDocument

main_buttons = [[
        InlineKeyboardButton('🕷 ᴄᴏᴅᴇ ᴀʀᴛɪꜱᴀɴ', url='https://t.me/SHUBHAM_X_OFFICIAL')
        ],[
        InlineKeyboardButton('👨‍💻 ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ', url='https://t.me/The_creator_SUpport_group'),
        InlineKeyboardButton('🔄 ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ', url='https://t.me/The_creator_bot')
        ],[
        InlineKeyboardButton('🆘 ʜᴇʟᴘ', callback_data='help'),
        InlineKeyboardButton('ℹ️ ᴀʙᴏᴜᴛ', callback_data='about')
        ],[
        InlineKeyboardButton('🆘 ʜᴇʟᴘ', callback_data='donate')
        ],[
        InlineKeyboardButton('⚙️ ꜱᴇᴛᴛɪɴɢꜱ', callback_data='settings#main')
        ]]

buttons = [[
        InlineKeyboardButton('🕸 ᴄᴏᴅᴇ ᴀʀᴛɪꜱᴀɴ', url='https://t.me/Shubham_x_official'),
        InlineKeyboardButton('💳 ʙᴜʏ ꜱᴏᴜʀᴄᴇ ᴄᴏᴅᴇ', url='https://t.me/Shubham_x_official')
        ]]


#===================Start Function===================#

@Client.on_message(filters.private & filters.command(['start']))
async def start(client, message):
    user = message.from_user
    
    # Fetch the picture from the provided URL
    picture_url = "https://te.legra.ph/Donate-Us-07-05"
    
    # Send the picture with the start message
    await client.send_photo(
        chat_id=message.chat.id,
        photo=picture_url,
        caption=Translation.START_TXT.format(message.from_user.first_name),
        reply_markup=InlineKeyboardMarkup(main_buttons)
    )
    
    # Check if the user exists in the database and add if not
    if not await db.is_user_exist(user.id):
        await db.add_user(user.id, user.first_name)


#==================Restart Function==================#

@Client.on_message(filters.private & filters.command(['restart']) & filters.user(Config.BOT_OWNER_ID))
async def restart(client, message):
    msg = await message.reply_text(
        text="<i>Trying to restarting.....</i>"
    )
    await asyncio.sleep(5)
    await msg.edit("<i>Server restarted successfully ✅</i>")
    os.execl(sys.executable, sys.executable, *sys.argv)

#===================HELP Function===================#

@Client.on_message(filters.command('help'))
async def help(client, message):
    user = message.from_user
    if not await db.is_user_exist(user.id):
        await db.add_user(user.id, user.first_name)
    
    # Fetch the picture from the provided URL
    picture_url = "https://te.legra.ph/Donate-Us-07-05"
    
    # Send the picture along with the help message
    await message.reply_photo(
        photo=picture_url,
        caption=Translation.HELP_TXT.format(message.from_user.first_name),
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    
#==================Callback Functions==================#

@Client.on_callback_query(filters.regex(r'^help'))
async def helpcb(bot, query):
    await query.message.edit_text(
        text=Translation.HELP_TXT,
        reply_markup=InlineKeyboardMarkup(
            [[
            InlineKeyboardButton('ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴍᴇ ❓', callback_data='how_to_use')
            ],[
            InlineKeyboardButton('⚙️ sᴇᴛᴛɪɴɢs ', callback_data='settings#main'),
            InlineKeyboardButton('📜 sᴛᴀᴛᴜs ', callback_data='status')
            ],[
            InlineKeyboardButton('↩ ʙᴀᴄᴋ', callback_data='back')
            ]]
        ))

@Client.on_callback_query(filters.regex(r'^how_to_use'))
async def how_to_use(bot, query):
    await query.message.edit_text(
        text=Translation.HOW_USE_TXT,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('↩ Back', callback_data='help')]]),
        disable_web_page_preview=True
    )

@Client.on_callback_query(filters.regex(r'^back'))
async def back(bot, query):
    reply_markup = InlineKeyboardMarkup(main_buttons)
    await query.message.edit_text(
       reply_markup=reply_markup,
       text=Translation.START_TXT.format(
                query.from_user.first_name))

@Client.on_callback_query(filters.regex(r'^about'))
async def about(bot, query):
    await query.message.edit_text(
        text=Translation.ABOUT_TXT.format(my_name='Public Forward',python_version=python_version(),pyrogram_version=pyrogram_version,mongodb_version=await mongodb_version()),
        reply_markup=InlineKeyboardMarkup(
            [[
            InlineKeyboardButton('🕷 ᴄᴏᴅᴇ ᴀʀᴛɪꜱᴀɴ', url='https://t.me/Shubham_X_official'),
            InlineKeyboardButton('💳 ʙᴜʏ ꜱᴏᴜʀᴄᴇ ᴄᴏᴅᴇ', url='https://t.me/Shubham_X_official')
            ],[
            InlineKeyboardButton('↩ ʙᴀᴄᴋ', callback_data='back')
            ]]
        ),
        disable_web_page_preview=True,
        parse_mode=enums.ParseMode.HTML,
                    )

@Client.on_callback_query(filters.regex(r'^status'))
async def status(bot, query):
    users_count, bots_count = await db.total_users_bots_count()
    total_channels = await db.total_channels()
    await query.message.edit_text(
        text=Translation.STATUS_TXT.format(users_count, bots_count, temp.forwardings, total_channels, temp.BANNED_USERS ),
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton('↩ Back', callback_data='help')]]),
        parse_mode=enums.ParseMode.HTML,
        disable_web_page_preview=True,
    )
