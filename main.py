from fbchat import Client
import config
import configTg
import configFb
import subprocess

from fbchat.models import *

import telepot
from telepot.loop import MessageLoop


bot = telepot.Bot(config.botToken)
chan = {}
chanTG = configTg.chanTG
chanFB = configFb.chanFB

class TgBot(Client):
    def onMessage(self,mid, author_id, message, message_object, thread_id, thread_type, ts, metadata, msg):
        author = self.fetchUserInfo(author_id)[author_id]
        if thread_id not in chanTG:
            bot.sendMessage(config.idTg,'Message provenant du chan: ' + str(chan[thread_id]))
            bot.sendMessage(config.idTg,'<' + author.name + '>: ' + message)
            bot.sendMessage(config.idTg,'Créez un nouveau groupe avec /init ' + str(thread_id) +' <type>')
            bot.sendMessage(config.idTg,'<type> vaut USER,PAGE,ROOM,GROUP')
        elif author_id is not config.idFb:
          bot.sendMessage(chanTG[thread_id],'<' + author.name + '>: ' + message)

client = TgBot(config.login, config.password)

def handle(msg):
    if msg['text'].split(' ')[0] in ['/init']:
        if msg['from']['id'] == int(config.idTg):
            tmp = msg['text'].split(' ')
            if tmp[1] not in chanTG:
                if len(tmp) > 2:
                    chanTG[tmp[1]] = msg['chat']['id']
                    chanFB[msg['chat']['id']] = [tmp[1],tmp[2]]
                    bot.sendMessage(chanTG[tmp[1]],'Le chan est config billy')
                    subprocess.call("rm configFb.py configTg.py", shell=True)
                    subprocess.call("touch configFb.py configTg.py", shell=True)
                    with open('configTg.py','r+') as f:
                        f.write("chanTG =" + str(chanTG))
                    with open('configFb.py','r+') as f:
                        f.write("chanFB =" + str(chanFB))
                else:
                    bot.sendMessage(msg['chat']['id'],'Manque le num')
            else:
                bot.sendMessage(chanTG[tmp[1]],'Déjà fait billy')
        else:
            bot.sendMessage(config.idTg,'Qui est tu ?')
    else:
        tmp = chanFB[msg['chat']['id']]
        a = ThreadType.USER
        if tmp[1] in 'USER':
            a = ThreadType.USER
        elif tmp[1] in 'GROUP':
            a = ThreadType.GROUP
        elif tmp[1] in 'ROOM':
            a = ThreadType.ROOM
        elif tmp[1] in 'PAGE':
            a = ThreadType.PAGE
        client.send(Message(text=msg['text']), thread_id=tmp[0],thread_type=a)
print(client)
MessageLoop(bot, handle).run_as_thread(allowed_updates=[])
client.listen()
