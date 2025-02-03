from .synta_mui import SyntaxMUI

_app_instance = SyntaxMUI()
write = _app_instance.write
run = _app_instance.run
text_input = _app_instance.text_input
button = _app_instance.button
set_widget_position = _app_instance.set_widget_position
clear_chat_history = _app_instance.clear_chat_history
stream_chat = _app_instance.stream_chat

run = _app_instance.run
get_text_input_value = _app_instance.get_text_input_value
get_chat_history = _app_instance.get_chat_history
clear_text_imput  = _app_instance.clear_text_input_value

# app = _app_instance.app

# class _StateProxy:
#     """
#     A proxy object that passes dictionary operations to 
#     _app_instance.state (the session-based dict).
#     """
#     def __contains__(self, key):
#         return key in _app_instance.state

#     def __getitem__(self, key):
#         return _app_instance.state[key]

#     def __setitem__(self, key, value):
#         _app_instance.state[key] = value

#     def __delitem__(self, key):
#         del _app_instance.state[key]

#     def get(self, key, default=None):
#         return _app_instance.state.get(key, default)

#     def keys(self):
#         return _app_instance.state.keys()

#     def items(self):
#         return _app_instance.state.items()

#     def __repr__(self):
#         return repr(_app_instance.state)

# # Our global 'state' object.
# state = _StateProxy()

__all__ = [
    "write", "run", "text_input", "button", 
    "set_widget_position", "clear_chat_history",
    "state"
]
