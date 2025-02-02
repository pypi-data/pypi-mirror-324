# syntaxmatrix/__init__.py
from .synta_mui import SyntaxMUI

_app_instance = SyntaxMUI()
write = _app_instance.write
run = _app_instance.run
text_input = _app_instance.text_input
button = _app_instance.button
set_widget_position = _app_instance.set_widget_position
clear_chat_history = _app_instance.clear_chat_history

