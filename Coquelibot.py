
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

import re

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

import colourdec



class Coquelibot():

    def start(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text=self.greatings)

    def help(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text=self.helper)
        
    def echo(self, bot, update):
        text = update.message.text
        if text != None :
            if re.match(r"^What is [a-zA-Z]+ \?$", text):
                rColour = text.split()[-2]
                try :
                    
                    img = colourdec.createMonocolourImg(rColour.lower())
                    img.save(self.outputLocation+'output.jpg')
                    bot.send_photo(chat_id=update.message.chat_id, photo=open(self.outputLocation+'output.jpg', 'rb'))
                except ValueError as e:
                    bot.send_message(chat_id=update.message.chat_id, text=rColour +" isn't a colour i could recognized, sorry")
    def unknown(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")
    def photo_analyze(self, bot, update):
        file_id = update.message.photo[1].file_id
        self.imgid+=1
        bot.getFile(file_id).download(self.saveLocation+'image'+str(self.imgid)+'.jpg')
        cname, img, rgb = colourdec.displayColor(self.saveLocation+'image'+str(self.imgid)+'.jpg', 5)
        text = update.message.caption
        if text != None :
            if re.match(r"^[a-zA-Z]+ or [a-zA-Z]+ \?$", text):
                rColour1 = text.split()[0]
                rColour2 = text.split()[-2]
                try :
                    bestColor = colourdec.whichColour(rColour1, rColour2, rgb)
                    print(bestColor)
                    bot.send_message(chat_id=update.message.chat_id, text="This image is more " + bestColor + ".")
                    
                except ValueError as e:
                    bot.send_message(chat_id=update.message.chat_id, text="I couldn't recognized that color, sorry")
        else :
            print(text)
            img.save(self.outputLocation+'output.jpg')
            bot.send_photo(chat_id=update.message.chat_id, photo=open(self.outputLocation+'output.jpg', 'rb'))
            if cname == 'grey':
                bot.send_message(chat_id=update.message.chat_id, text="It's "+ cname + "! it looks a bit like me !")
            else :
                bot.send_message(chat_id=update.message.chat_id, text=cname + " is a very sweet color. I would dress my baby with it.")

    def __init__(self):
        self.admin = 190711873
        self.imgid = 0
        self.token = token=''#toComplete
        self.saveLocation = ''#toComplete
        self.outputLocation = ''#toComplete
        self.updater = Updater(token=self.token)
        self.dispatcher = self.updater.dispatcher

        self.greatings ="""
Hi ! I'm a Coquelibot, a bot dedicated to analyze your pictures and tell you the real colour of your object !
To get a full list of my functionalities, type /help !

            """

        self.helper ="""
______________________________________________
Send any photo to get it analysed !
By default, you will receive the dominant colour of the picture along with a sample of it.
If you specify "colour1 or colour2 ?" You will be told to which of colour1 and colour2 the dominant colour of your image is the closest.
______________________________________________
If you ask "What is colour ?" where colour is a standard colour name, you will receive a sample of it.

            """
        
        #Handlers defined
        self.dispatcher.add_handler(CommandHandler('start', self.start))
        
        self.dispatcher.add_handler(CommandHandler('help', self.help))

        self.dispatcher.add_handler(MessageHandler(Filters.photo, self.photo_analyze))

        self.dispatcher.add_handler(MessageHandler(Filters.text, self.echo))

        self.dispatcher.add_handler(MessageHandler(Filters.command, self.unknown))

        self.updater.start_polling()

if __name__ == '__main__' :
    Coquelibot()
