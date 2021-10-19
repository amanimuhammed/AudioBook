import os 
import pyrogram
import PyPDF2
import time
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.types import User, Message, Document 
from gtts import gTTS

bughunter0 = Client(
    "Audio-BOT",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)

START_STR = """
**Hi {},\nI'm AudioBook Bot. Send Me a Pdf to Convert to AudioBook\n\n🏷️ Maintained By: @Amani_m_h_d**
"""
ABOUT = """
➥**My Name :** `AudioBook Bot🤓`
➥**Dev : [Amani Muhammed](https://t.me/Amani_m_h_d)**
➥**Channel : [Botz Hub](https://t.me/My_Test_Botz)**
➥**Credits :** `Everyone in this journey`
➥**Language :** `Python3`
➥**Library : [Pyrogram](https://docs.pyrogram.org/)**
➥**Server : [Heroku](https://herokuapp.com/)**
➥**Source Code : [👉 Click Here](http://t.me/nokkiirunnoippokittum)**
➥**Follow on Insta: [Follow me](https://www.instagram.com/amani_m_h_d)**
       
         **📜Quote :** `ക്ഷമ വേണം സമയം എടുക്കും 🙃™️`
"""
HELP = """
**Hey, Send me a pdf file to Move on.\n\n🏷️ Maintained By: @Amani_m_h_d**
"""

DOWNLOAD_LOCATION = os.environ.get("DOWNLOAD_LOCATION", "./DOWNLOADS/AudioBoT/")

Disclaimer = """ Disclaimer Notice , This Audio Is Generated automatically Through AudioBook Bot, Join Botzhub for More Bots .    You are Now Listening to your Audio  ."""
  
Thanks = """ Thats the End of Your Audio Book, Join Botzhub To find more Interesting bots , And Thanks for Using this Service"""

START_BUTTON = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('ABOUT',callback_data='cbabout'),
        InlineKeyboardButton('HELP',callback_data='cbhelp')
        ],
        [
        InlineKeyboardButton('↗ Join Here ↗', url='https://t.me/my_test_botz'),
        ]]
        
    )
CLOSE_BUTTON = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Back',callback_data='cbclose'),
        ]]
    )

CHANNEL_BUTTON = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('↗ Join Here ↗', url='https://t.me/my_test_botz')
        ]]
    )

@bughunter0.on_message(filters.command(["start"]))
async def start(bot,update):
               await update.reply_text(
               text=START_STR.format(update.from_user.mention),
               disable_web_page_preview=True,
               reply_markup=START_BUTTON,
               quote=True
               )
	
	
@bughunter0.on_callback_query() # callbackQuery()
async def cb_data(bot, update):  
    if update.data == "cbhelp":
        await update.message.edit_text(
            text=HELP,
            reply_markup=CLOSE_BUTTON,
            disable_web_page_preview=True
        )
    elif update.data == "cbabout":
        await update.message.edit_text(
            text=ABOUT,
            reply_markup=CLOSE_BUTTON,
            disable_web_page_preview=True
        )
    else:
        await update.message.edit_text(
            text=START_STR.format(update.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=START_BUTTON
        )
        
@bughunter0.on_message(filters.command(["audiobook"])) # PdfToText 
async def pdf_to_text(bot, message):
 try:
           if message.reply_to_message:
                pdf_path = DOWNLOAD_LOCATION + f"{message.chat.id}.pdf" #pdfFileObject
                txt = await message.reply("Downloading.....")
                await message.reply_to_message.download(pdf_path)  
                await txt.edit("Downloaded File")
                pdf = open(pdf_path,'rb')
                pdf_reader = PyPDF2.PdfFileReader(pdf) #pdfReaderObject
                await txt.edit("Getting Number of Pages....")
                num_of_pages = pdf_reader.getNumPages() # Number of Pages               
                await txt.edit(f"Found {num_of_pages} Page")
                page_no = pdf_reader.getPage(0) # pageObject
                await txt.edit("Finding Text from Pdf File... ")
                page_content = """ """ # EmptyString   
                chat_id = message.chat.id
                with open(f'{message.chat.id}.txt', 'a+') as text_path:   
                  for page in range (0,num_of_pages):              
                      page_no = pdf_reader.getPage(page) # Iteration of page number
                      page_content += page_no.extractText()
                await txt.edit(f"Creating Your Audio Book...\n Please Don't Do Anything \n**Join :** `@My_Test_Botz`")
                output_text = Disclaimer + page_content + Thanks
              # Change Voice by editing the Language
                language = 'en-in'  # 'en': ['en-us', 'en-ca', 'en-uk', 'en-gb', 'en-au', 'en-gh', 'en-in',
                                    # 'en-ie', 'en-nz', 'en-ng', 'en-ph', 'en-za', 'en-tz'],
                tts_file = gTTS(text=output_text, lang=language, slow=False) 
                tts_file.save(f"{message.chat.id}.mp3")      
                with open(f"{message.chat.id}.mp3", "rb") as speech:
                      await bot.send_voice(chat_id, speech, caption ="@Amani_m_h_d",reply_markup=CHANNEL_BUTTON)   
                await txt.edit("Join @my_test_botz")    
                os.remove(pdf_path)  
                
                
           else :
                await message.reply("Please Reply to PDF file")
 except Exception as error :
           print(error)
           await txt.delete()
           os.remove(pdf_path)
         
bughunter0.run()
 	
