
# syntaxmatrix/__init__.py
from .synta_mui import SyntaxMUI

_app_instance = SyntaxMUI()

# Standard exports so devs can do: import syntaxmatrix as st
run = _app_instance.run
text_input = _app_instance.text_input
button = _app_instance.button
set_widget_position = _app_instance.set_widget_position
clear_chat_history = _app_instance.clear_chat_history

# If you want text input helpers
get_text_input_value = _app_instance.get_text_input_value
clear_text_input_value = _app_instance.clear_text_input_value

# Chat history helpers
get_chat_history = _app_instance.get_chat_history
set_chat_history = _app_instance.set_chat_history

# Final streaming function
stream_chat = _app_instance.stream_chat
