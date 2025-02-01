from rich.console import Console
from typing import Optional
from byzerllm.utils import format_str_jinja2
from autocoder.common.auto_coder_lang import get_message
from autocoder.chat_auto_coder_lang import get_message as get_chat_message
class Printer:
    def __init__(self,console:Optional[Console]=None):
        if console is None:
            self.console = Console()
        else:
            self.console = console

    def get_message_from_key(self, key: str):
        try:
            return get_message(key)
        except Exception as e:
            return get_chat_message(key)

    def print_in_terminal(self, key: str, style: str = None,**kwargs):     
        try:
            if style:
                self.console.print(format_str_jinja2(self.get_message_from_key(key),**kwargs), style=style)
            else:
                self.console.print(format_str_jinja2(self.get_message_from_key(key),**kwargs))
        except Exception as e:
            print(self.get_message_from_key(key))

    
    def print_str_in_terminal(self, content: str, style: str = None):     
        try:
            if style:
                self.console.print(content, style=style)
            else:
                self.console.print(content)
        except Exception as e:
            print(content)        