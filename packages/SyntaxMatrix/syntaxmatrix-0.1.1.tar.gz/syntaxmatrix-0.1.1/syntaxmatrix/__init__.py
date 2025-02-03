from .synta_mui import SyntaxMUI

_app_instance = SyntaxMUI()
write = _app_instance.write
run = _app_instance.run
text_input = _app_instance.text_input
button = _app_instance.button
set_widget_position = _app_instance.set_widget_position
clear_chat_history = _app_instance.clear_chat_history

# New helper functions to abstract session access:
def get_text_input_value(key, default=""):
    return _app_instance._get_text_input_value(key, default)

def clear_text_input_value(key):
    return _app_instance._clear_text_input_value(key)

def get_chat_history():
    return _app_instance._get_chat_history()

def set_chat_history(history):
    return _app_instance._set_chat_history(history)

# Global API.
__all__ = [
    "write", "run", "text_input", "button", "set_widget_position", "clear_chat_history",
    "get_text_input_value", "clear_text_input_value", "get_chat_history", "set_chat_history"
]
