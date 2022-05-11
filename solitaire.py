# coding: utf-8
from typing import Optional
import re

from ehforwarderbot import Middleware, Message, coordinator
from ehforwarderbot.message import MsgType
from ehforwarderbot.types import ModuleID, InstanceID

class MatrixLauMiddleware(Middleware):
    """
    EFB Middleware - Solitaire Middleware
    """

    middleware_id: ModuleID = ModuleID("solitaire.MatrixLauMiddleware")
    middleware_name: str = "Solitaire Middleware"
    __version__: str = '1.3.0'

    def __init__(self, instance_id: Optional[InstanceID] = None):
        global last_solitaire
        last_solitaire = {
            "群名": "接龙信息",
        }

        global solitaire_keyword
        '''接龙关键词'''
        solitaire_keyword = {
            "#接龍":3,
            "#接龙":3,
        }

        global solitaire_process
        '''接龙已处理关键词'''
        solitaire_process = {
            "solitaire_process":1, #0为未处理 1为已处理
        }

        '''接龙命令'''
        global solitaire_command
        solitaire_command = "jl`"

        super().__init__(instance_id)

    @staticmethod
    def sent_by_master(message: Message) -> bool:
        return message.deliver_to != coordinator.master

    def process_message(self, message: Message) -> Optional[Message]:
        flag = True
        if message.type == MsgType.Text and "Group" in type(message.chat).__name__:
            global last_solitaire
            for key, value in solitaire_keyword.items():
                if key in message.text:
                    if last_solitaire.get(message.chat.name,'') == '':
                        last_solitaire[message.chat.name] = message
                        return message
                    # elif last_solitaire[message.chat.name].text in message.text \
                    elif self.reduce_solitaire(last_solitaire[message.chat.name].text) in message.text \
                        and last_solitaire.get(message.chat.name).text != message.text:
                        global solitaire_process
                        if message.vendor_specific == '' \
                            or message.vendor_specific.get('solitaire_process',0) == 1\
                            or self.sent_by_master(message):
                            return message
                        flag = False
                        # message = self.process_samenum(message)
                        self.reflash_solitaire(message)
                    else:
                        last_solitaire[message.chat.name] = message
                        return message
            global solitaire_command
            if message.text.startswith(solitaire_command):
                name = message.text.replace(solitaire_command, '')
                name = name.replace(' ', '')
                if message.target != None:
                    message.text = message.target.text
                elif last_solitaire.get(message.chat.name,'') != '':
                    message.text = last_solitaire[message.chat.name].text
                else:
                    return None
                numlist = message.text.split('\n')
                length = len(numlist)
                numlist = numlist[length-1].split('.')
                message.text += '\n' + str(int(numlist[0])+1) + '. '+name
                if last_solitaire.get(message.chat.name,'') == '' and message.target != None:
                    last_solitaire[message.chat.name] = message.target
                if message.target != None and last_solitaire[message.chat.name].text != message.target.text:
                    last_solitaire[message.chat.name] = message.target
                message.target = None
                self.reflash_solitaire(message)
        if flag:
            return message

    def reflash_solitaire(self, message:Message):
        global last_solitaire
        last_solitaire[message.chat.name].text = message.text
        edited = last_solitaire[message.chat.name]
        edited.edit = True
        edited.vendor_specific['solitaire_process'] = 1
        coordinator.send_message(edited)

    def process_samenum(self, message:Message):
        ori_message = message
        global last_solitaire
        if last_solitaire.get(message.chat.name, '') == '':
            return ori_message
        solitaire_reduce = re.findall('\d.*\.\s.*.\n', message.text)
        last_solitaire_reduce = re.findall('\d.*\.\s.*.\n', last_solitaire[message.chat.name].text)
        # if last_solitaire.get(message.chat.name+'_reduce','') == '':
        #     last_solitaire[message.chat.name+'_reduce'] = solitaire_reduce
        # elif last_solitaire[message.chat.name+'_reduce'] \
        #     not in last_solitaire[message.chat.name].text:
        #     last_solitaire[message.chat.name+'_reduce'] = solitaire_reduce

        if solitaire_reduce == last_solitaire_reduce \
            or solitaire_reduce in last_solitaire_reduce:
            process_list = message.text.split('\n')
            samerow = process_list[len(process_list)-1]
            rowlist = samerow.split('.')

            rowlist[0] = str(int(len(last_solitaire_reduce)) + 2) +'.'
            newrow = ''.join(rowlist)
            message.text = last_solitaire[message.chat.name].text + '\n' + newrow
        elif last_solitaire_reduce in solitaire_reduce:
            return ori_message
        return message

    
    def reduce_solitaire(self, text):
        return ''.join(re.findall('\d.*\.\s.*.\n', text))



        

