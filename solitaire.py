# coding: utf-8
from typing import Optional

from ehforwarderbot import Middleware, Message, coordinator
from ehforwarderbot.message import MsgType
from ehforwarderbot.types import ModuleID, InstanceID

class MatrixLauMiddleware(Middleware):
    """
    Solitaire Middleware
    """

    middleware_id: ModuleID = ModuleID("solitaire.MatrixLauMiddleware")
    middleware_name: str = "Solitaire Middleware"
    __version__: str = '1.1.0'

    def __init__(self, instance_id: Optional[InstanceID] = None):
        global last_solitaire
        last_solitaire = ''

        global solitaire
        '''接龙关键词'''
        solitaire = {
            "#接龍":3,
            "#接龙":3,
        }

        global solitaire_process
        '''接龙已处理关键词'''
        solitaire_process = {
            "solitaire_process":1, #0为未处理 1为已处理
        }

        super().__init__(instance_id)

    @staticmethod
    def sent_by_master(message: Message) -> bool:
        return message.deliver_to != coordinator.master

    def process_message(self, message: Message) -> Optional[Message]:
        flag = True
        if message.type == MsgType.Text and "Group" in type(message.chat).__name__:
            global last_solitaire
            for key, value in solitaire.items():
                if key in message.text:
                    if last_solitaire == '':
                        last_solitaire = message
                        return message
                    elif last_solitaire.text in message.text and last_solitaire.text != message.text:
                        global solitaire_process
                        if message.vendor_specific != '':
                            if message.vendor_specific.get('solitaire_process',0) == 1:
                                return message
                        flag = False
                        last_solitaire.text = message.text
                        edited = last_solitaire
                        edited.edit = True
                        edited.vendor_specific['solitaire_process'] = 1
                        coordinator.send_message(edited)
                    else:
                        last_solitaire = message
                        return message
        if flag:
            return message
            
