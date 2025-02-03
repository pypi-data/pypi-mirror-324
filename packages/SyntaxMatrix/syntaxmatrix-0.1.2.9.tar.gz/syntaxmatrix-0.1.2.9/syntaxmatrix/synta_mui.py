# syntaxmatrix/synta_mui.py
import os
import uuid
import time
import openai

from flask import Flask, request, session, has_request_context, render_template_string, redirect, url_for
from collections import OrderedDict

class SyntaxMUI:
    def __init__(self, title="SyntaxMUI App"):
        self.app = Flask(__name__)
        self.app.secret_key = "syntaxmatrix_secret"  # for session usage
        self.title = title

        # For normal st.write() or pinned chat, we store “content” in memory.
        self.content_buffer = []
        # For text_input, button, etc.:
        self.widgets = OrderedDict()

        # For streaming: one global route ("/_syntaxmatrix_stream")
        # plus two dicts for storing data and final text by a random ID
        self._stream_data = {}
        self._stream_results = {}

        # Let’s define a single streaming route once, at startup.
        self._init_streaming_route()

        # Build the default route that renders the pinned widget form, chat logs, etc.
        self._init_index_route()

    def _init_streaming_route(self):
        """Create exactly ONE route '/_syntaxmatrix_stream', so we never define routes after handling requests."""
        @self.app.route("/_syntaxmatrix_stream", methods=["POST"])
        def global_stream():
            if "stream_id" not in request.form:
                return "[Error] Missing stream_id", 400
            stream_id = request.form["stream_id"]
            if stream_id not in self._stream_data:
                return "[Error] Invalid stream_id", 400

            data = self._stream_data[stream_id]
            # retrieve the openai params
            llm_model = data["model"]
            messages = data["messages"]
            temperature = data["temperature"]
            max_tokens = data["max_tokens"]
            extra_kwargs = data["extra_kwargs"]

            final_chunks = []

            def generate():
                try:
                    # stream from openai
                    response = openai.ChatCompletion.create(
                        model=llm_model,
                        messages=messages,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        stream=True,
                        **extra_kwargs
                    )
                    for chunk in response:
                        if ('choices' in chunk 
                            and len(chunk['choices']) > 0 
                            and 'delta' in chunk['choices'][0] 
                            and 'content' in chunk['choices'][0]['delta']):
                            token_text = chunk['choices'][0]['delta']['content']
                            final_chunks.append(token_text)
                            yield token_text
                except Exception as e:
                    yield f"\n[OpenAI streaming error: {e}]"

            def finalize(_):
                # store final text in self._stream_results
                self._stream_results[stream_id] = "".join(final_chunks)
                # remove the data from memory
                if stream_id in self._stream_data:
                    del self._stream_data[stream_id]

            resp = self.app.response_class(generate(), mimetype="text/plain")
            resp.call_on_close(lambda: finalize(None))
            return resp

    def _init_index_route(self):
        """A minimal route that processes widget form submissions 
        and calls the pinned layout.  This is enough to 
        handle the text_input, button callbacks, etc."""
        @self.app.route("/", methods=["GET", "POST"])
        def index():
            from flask import request
            if request.method == "POST":
                # Handle form submission for text inputs, buttons, etc.
                for key, widget in self.widgets.items():
                    if widget["type"] == "text_input":
                        session[key] = request.form.get(key, widget["default"])
                    elif widget["type"] == "button":
                        # If the user clicked this button name
                        if key in request.form and widget["callback"]:
                            widget["callback"]()
                return redirect(url_for("index"))

            # Build a pinned form with the text inputs & buttons
            widget_html = self._render_widgets()
            # Build the chat messages from session (like st.state["messages"])
            chat_html = self._render_chat()

            # Some minimal style & layout
            page_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>{self.title}</title>
                <style>
                  body {{
                      font-family: Arial, sans-serif; 
                      margin: 0; 
                      padding: 0;
                      background: #f7f7f7;
                  }}
                  #chat-container {{
                      width: 80%;
                      max-width: 800px;
                      margin: 10px auto;
                      background: #fff;
                      border-radius: 6px;
                      min-height: 400px;
                      padding: 10px;
                      box-shadow: 1px 1px 5px rgba(0,0,0,0.2);
                  }}
                  .chat-message {{
                      margin: 10px;
                      padding: 10px 15px;
                      border-radius: 10px;
                      max-width: 70%;
                      clear: both;
                      font-family: sans-serif;
                      line-height: 1.4;
                      box-shadow: 1px 1px 3px rgba(0,0,0,0.1);
                  }}
                  .chat-message.user {{
                      background-color: #dcf8c6;
                      float: right;
                      text-align: right;
                  }}
                  .chat-message.bot {{
                      background-color: #ffffff;
                      float: left;
                      text-align: left;
                      border: 1px solid #ddd;
                  }}
                  #widget-container {{
                      width: 80%;
                      max-width: 800px;
                      margin: 10px auto;
                      background: #fff;
                      border-radius: 6px;
                      padding: 10px;
                      box-shadow: 1px 1px 5px rgba(0,0,0,0.2);
                      position: fixed;
                      bottom: 0;
                      left: 50%;
                      transform: translateX(-50%);
                  }}
                </style>
            </head>
            <body>
                <div id="chat-container">{chat_html}</div>
                <div id="widget-container">{widget_html}</div>
            </body>
            </html>
            """
            return page_html

    def _render_widgets(self):
        """Generate a simple <form> with text inputs & buttons in a row."""
        if not self.widgets:
            return ""
        text_input_html = ""
        button_html = ""
        for key, widget in self.widgets.items():
            if widget["type"] == "text_input":
                current_value = session.get(key, widget["default"])
                text_input_html += f"""
                <div style="margin-bottom:10px;">
                  <textarea name="{key}" style="width:90%;height:50px;">{current_value}</textarea>
                </div>
                """
            elif widget["type"] == "button":
                button_html += f"""
                <div style="display:inline-block;margin-right:10px;">
                  <button type="submit" name="{key}" value="clicked">{widget["label"]}</button>
                </div>
                """
        combined = f"""
        <form method="POST">
          {text_input_html}
          {button_html}
        </form>
        """
        return combined

    def _render_chat(self):
        """Render the chat history from session['messages'], if any."""
        chat_html = ""
        messages = session.get("messages", [])
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            role_class = "user" if role == "user" else "bot"
            chat_html += f"<div class='chat-message {role_class}'><strong>{role.capitalize()}:</strong> {content}</div>"
        return chat_html

    # ----------------------------
    #  Public methods for dev usage
    # ----------------------------

    def run(self, host="127.0.0.1", port=5000):
        self.app.run(host=host, port=port, debug=False)

    def text_input(self, key, label, default=""):
        if key not in self.widgets:
            self.widgets[key] = {"type": "text_input", "key": key, "label": label, "default": default}

    def button(self, key, label, callback=None):
        if key not in self.widgets:
            self.widgets[key] = {"type": "button", "key": key, "label": label, "callback": callback}

    def get_text_input_value(self, key, default=""):
        if not has_request_context():
            return default
        return session.get(key, default)

    def stream_chat(self, model, messages, temperature=0.7, max_tokens=100, **kwargs):
        """
        1) Generate a random ID, store data in self._stream_data[stream_id].
        2) Insert a JS snippet that calls /_syntaxmatrix_stream with that ID.
        3) Wait for final text in self._stream_results. Return it so you can store in session.
        """
        if not has_request_context():
            raise RuntimeError("stream_chat must be called within request context!")
        stream_id = uuid.uuid4().hex
        self._stream_data[stream_id] = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "extra_kwargs": kwargs
        }
        self._stream_results[stream_id] = ""

        js = f"""
        <script>
        (function() {{
          // create a new BOT bubble in the chat container
          var chatContainer = document.getElementById("chat-container");
          var botDiv = document.createElement("div");
          botDiv.className = "chat-message bot";
          botDiv.innerHTML = "<strong>Bot:</strong> ";
          chatContainer.appendChild(botDiv);

          var formData = new FormData();
          formData.append("stream_id", "{stream_id}");
          fetch("/_syntaxmatrix_stream", {{
            method: "POST",
            body: formData
          }})
          .then(response => {{
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            function readChunk() {{
              reader.read().then(({{
                done, value
              }}) => {{
                if (done) return;
                let chunk = decoder.decode(value);
                botDiv.innerHTML += chunk;
                window.scrollTo(0, document.body.scrollHeight);
                readChunk();
              }});
            }}
            readChunk();
          }})
          .catch(err => {{
            console.error("stream_chat error:", err);
            botDiv.innerHTML += "<br>[Error: " + err + "]";
          }});
        }})();
        </script>
        """
        # Insert the snippet so it runs after page load
        self.content_buffer.append(js)

        # We'll wait up to ~5 seconds to get final text
        for _ in range(50):
            final_text = self._stream_results.get(stream_id, "")
            if final_text:
                break
            time.sleep(0.1)

        return self._stream_results.pop(stream_id, "")

    # The user’s “messages” list in session:
    def add_message(self, role, content):
        if "messages" not in session:
            session["messages"] = []
        session["messages"].append({"role": role, "content": content})
        session.modified = True

    def clear_messages(self):
        session["messages"] = []
        session.modified = True


#################################################################

# # syntaxmatrix/synta_mui.py

# from flask import Flask, render_template_string, request, session, redirect, url_for, has_request_context
# from collections import OrderedDict
# import uuid
# import time

# class SyntaxMUI:
#     def __init__(self, title="SyntaxMUI App", nav_items=None, widget_position="top"):
#         self.app = Flask(__name__)
#         self.app.secret_key = "syntaxmatrix_secret"  # For session usage
#         self.title = title
#         self.nav_items = nav_items or {"Home": self.home_page}
#         self.content_buffer = []  # For st.write() content
#         self.widgets = OrderedDict()  # For text inputs, buttons, etc.
#         self.widget_position = widget_position

#         # For streaming:
#         self._stream_data = {}    # Dict: stream_id -> dict(llm, messages, etc.)
#         self._stream_results = {} # Dict: stream_id -> final text
#         self.init_streaming_route()

#         # Setup routes for index, admin, etc.
#         self.setup_routes()

#     # ----------------------------------------------------------------
#     # 1) The single, global streaming route
#     # ----------------------------------------------------------------
#     def init_streaming_route(self):
#         """
#         Creates /_syntaxmatrix_stream exactly once, so we never define routes after
#         the first request. This route uses an ID from the form data to fetch
#         LLM parameters from self._stream_data, calls stream=True, yields partial tokens,
#         and stores final text in self._stream_results.
#         """
#         @self.app.route("/_syntaxmatrix_stream", methods=["POST"])
#         def _global_stream_route():
#             form_data = request.form
#             stream_id = form_data.get("stream_id")
#             if not stream_id or stream_id not in self._stream_data:
#                 return "Invalid or missing stream_id", 400

#             data = self._stream_data[stream_id]
#             llm = data["llm"]
#             model = data["model"]
#             messages = data["messages"]
#             temperature = data["temperature"]
#             max_tokens = data["max_tokens"]
#             extra_kwargs = data["extra_kwargs"]

#             final_chunks = []

#             def generate():
#                 try:
#                     response = llm.chat.completions.create(
#                         model=model,
#                         messages=messages,
#                         temperature=temperature,
#                         max_tokens=max_tokens,
#                         stream=True,
#                         **extra_kwargs
#                     )
#                     for chunk in response:
#                         if ("choices" in chunk 
#                             and chunk["choices"] 
#                             and "delta" in chunk["choices"][0]
#                             and "content" in chunk["choices"][0]["delta"]):
#                             token_text = chunk["choices"][0]["delta"]["content"]
#                             final_chunks.append(token_text)
#                             yield token_text
#                 except Exception as e:
#                     yield f"\n[stream_chat error: {e}]"

#             def finalize(_):
#                 self._stream_results[stream_id] = "".join(final_chunks)
#                 # remove data from memory
#                 self._stream_data.pop(stream_id, None)

#             r = self.app.response_class(generate(), mimetype="text/plain")
#             r.call_on_close(lambda: finalize(None))
#             return r

#     # ----------------------------------------------------------------
#     # 2) The user-facing "stream_chat" function
#     # ----------------------------------------------------------------
#     def stream_chat(self, llm, model, messages, temperature=0.7, max_tokens=150, **kwargs):
#         """
#         Called by user code in a callback. 
#         1) We store the LLM data in self._stream_data keyed by stream_id.
#         2) Inject a small JS snippet that calls /_syntaxmatrix_stream with that stream_id.
#         3) Poll self._stream_results until we get the final text, then return it.
#         """
#         if not has_request_context():
#             raise RuntimeError("stream_chat(...) must be called within a request context.")

#         # 1) Generate a unique stream_id
#         stream_id = uuid.uuid4().hex

#         # 2) Store the data
#         self._stream_data[stream_id] = {
#             "llm": llm,
#             "model": model,
#             "messages": messages,
#             "temperature": temperature,
#             "max_tokens": max_tokens,
#             "extra_kwargs": kwargs,
#         }
#         self._stream_results[stream_id] = ""

#         # 3) Inject the JS snippet that calls /_syntaxmatrix_stream
#         js_snippet = f"""
#         <script>
#         (function() {{
#           var chatContainer = document.getElementById("chat-container");
#           var botDiv = document.createElement("div");
#           botDiv.className = "chat-message bot";
#           botDiv.innerHTML = "<strong>Bot:</strong> ";
#           chatContainer.appendChild(botDiv);

#           var formData = new FormData();
#           formData.append("stream_id", "{stream_id}");

#           fetch("/_syntaxmatrix_stream", {{
#             method: "POST",
#             body: formData
#           }})
#           .then(response => {{
#             const reader = response.body.getReader();
#             const decoder = new TextDecoder();
#             function readChunk() {{
#               reader.read().then(({{ done, value }}) => {{
#                 if (done) return;
#                 let chunk = decoder.decode(value);
#                 botDiv.innerHTML += chunk;
#                 window.scrollTo(0, document.body.scrollHeight);
#                 readChunk();
#               }});
#             }}
#             readChunk();
#           }})
#           .catch(err => {{
#             console.error("stream_chat error:", err);
#             botDiv.innerHTML += "<br>[Error: " + err + "]";
#           }});
#         }})();
#         </script>
#         """
#         self.write(js_snippet)

#         # 4) Poll for final text
#         for _ in range(50):  # ~5 seconds max
#             final_text = self._stream_results.get(stream_id, "")
#             if final_text:
#                 break
#             time.sleep(0.1)

#         # Remove from results and return
#         return self._stream_results.pop(stream_id, "")

#     # ----------------------------------------------------------------
#     # 3) Basic routes + widget system (like we had in prior examples)
#     # ----------------------------------------------------------------
#     def setup_routes(self):
#         # Make sure we don’t register twice:
#         if "index" in self.app.view_functions:
#             return

#         @self.app.route("/", methods=["GET", "POST"])
#         def index():
#             if request.method == "POST":
#                 # Process widgets
#                 for key, widget in self.widgets.items():
#                     if widget["type"] == "text_input":
#                         session[key] = request.form.get(key, widget["default"])
#                     elif widget["type"] == "button":
#                         if key in request.form and widget.get("callback"):
#                             widget["callback"]()
#                 return redirect(url_for("index"))

#             nav_html = "".join(f'<li><a href="/page/{item}">{item}</a></li>' for item in self.nav_items)
#             nav_html += '<li><a href="/admin">Admin</a></li>'

#             content = self.home_page()
#             widget_form_html = self.render_widgets()

#             auto_scroll_script = """
#             <script>
#               window.onload = function() {
#                 window.scrollTo(0, document.body.scrollHeight);
#               };
#             </script>
#             """

#             # Different layout if pinned at bottom or at top
#             if self.widget_position == "bottom":
#                 page_html = f"""
#                 <!DOCTYPE html>
#                 <html>
#                 <head>
#                   <title>{self.title}</title>
#                   <style>
#                     body {{
#                       font-family: Arial, sans-serif;
#                       margin: 0;
#                       padding-bottom: 140px;
#                     }}
#                     nav ul {{
#                       list-style-type: none;
#                       padding: 10px;
#                       background: #333;
#                     }}
#                     nav li {{
#                       display: inline;
#                       margin-right: 15px;
#                     }}
#                     nav li a {{
#                       color: #fff;
#                       text-decoration: none;
#                     }}
#                     #chat-container {{
#                       padding: 20px;
#                       background: #f7f7f7;
#                       min-height: 80vh;
#                       max-width: 800px;
#                       margin: 20px auto;
#                       border-radius: 10px;
#                       overflow-y: auto;
#                     }}
#                     #widget-container {{
#                       position: fixed;
#                       bottom: 0;
#                       left: 0;
#                       right: 0;
#                       background: #f9f9f9;
#                       border-top: 1px solid #ccc;
#                       padding: 10px;
#                       text-align: center;
#                     }}
#                     .chat-message {{
#                       margin: 10px;
#                       padding: 10px 15px;
#                       border-radius: 10px;
#                       max-width: 70%;
#                       clear: both;
#                       font-family: sans-serif;
#                       line-height: 1.4;
#                       box-shadow: 1px 1px 3px rgba(0,0,0,0.1);
#                     }}
#                     .chat-message.user {{
#                       background-color: #dcf8c6;
#                       float: right;
#                       text-align: right;
#                     }}
#                     .chat-message.bot {{
#                       background-color: #ffffff;
#                       float: left;
#                       text-align: left;
#                       border: 1px solid #ddd;
#                     }}
#                     .input textarea {{
#                       width: 90%;
#                       height: 60px;
#                       font-size: 16px;
#                       padding: 5px;
#                       box-sizing: border-box;
#                       resize: vertical;
#                     }}
#                     .button-container {{
#                       display: flex;
#                       justify-content: center;
#                       gap: 10px;
#                       margin-top: 10px;
#                     }}
#                     .button-container button {{
#                       font-size: 16px;
#                       padding: 10px 20px;
#                     }}
#                   </style>
#                 </head>
#                 <body>
#                   <nav><ul>{nav_html}</ul></nav>
#                   <div id="chat-container">
#                     {content}
#                   </div>
#                   <div id="widget-container">
#                     {widget_form_html}
#                   </div>
#                   {auto_scroll_script}
#                 </body>
#                 </html>
#                 """
#             else:
#                 page_html = f"""
#                 <!DOCTYPE html>
#                 <html>
#                 <head>
#                   <title>{self.title}</title>
#                   <style>
#                     body {{
#                       font-family: Arial, sans-serif;
#                     }}
#                     nav ul {{
#                       list-style-type: none;
#                       padding: 10px;
#                       background: #333;
#                     }}
#                     nav li {{
#                       display: inline;
#                       margin-right: 15px;
#                     }}
#                     nav li a {{
#                       color: #fff;
#                       text-decoration: none;
#                     }}
#                     #chat-container {{
#                       padding: 20px;
#                       background: #f7f7f7;
#                       min-height: 80vh;
#                       max-width: 800px;
#                       margin: 20px auto;
#                       border-radius: 10px;
#                       overflow-y: auto;
#                     }}
#                     .chat-message {{
#                       margin: 10px;
#                       padding: 10px 15px;
#                       border-radius: 10px;
#                       max-width: 70%;
#                       clear: both;
#                       font-family: sans-serif;
#                       line-height: 1.4;
#                       box-shadow: 1px 1px 3px rgba(0,0,0,0.1);
#                     }}
#                     .chat-message.user {{
#                       background-color: #dcf8c6;
#                       float: right;
#                       text-align: right;
#                     }}
#                     .chat-message.bot {{
#                       background-color: #ffffff;
#                       float: left;
#                       text-align: left;
#                       border: 1px solid #ddd;
#                     }}
#                     .input textarea {{
#                       width: 90%;
#                       height: 60px;
#                       font-size: 16px;
#                       padding: 5px;
#                       box-sizing: border-box;
#                       resize: vertical;
#                     }}
#                     .button-container {{
#                       display: flex;
#                       justify-content: center;
#                       gap: 10px;
#                       margin-top: 10px;
#                     }}
#                     .button-container button {{
#                       font-size: 16px;
#                       padding: 10px 20px;
#                     }}
#                   </style>
#                 </head>
#                 <body>
#                   <nav><ul>{nav_html}</ul></nav>
#                   <div>
#                     {widget_form_html}
#                   </div>
#                   <div id="chat-container">
#                     {content}
#                   </div>
#                   {auto_scroll_script}
#                 </body>
#                 </html>
#                 """
#             return render_template_string(page_html)

#         @self.app.route("/page/<page_name>")
#         def page(page_name):
#             if page_name in self.nav_items:
#                 return self.nav_items[page_name]()
#             return "Page not found", 404

#         @self.app.route("/admin", methods=["GET"])
#         def admin_panel():
#             return "Admin Panel Placeholder"

#     def render_widgets(self):
#         """Generate HTML for interactive widgets (text_input, button, etc.)."""
#         if not self.widgets:
#             return ""
#         text_input_html = ""
#         button_html = ""
#         for key, widget in self.widgets.items():
#             if widget["type"] == "text_input":
#                 current_value = session.get(key, widget["default"]) if has_request_context() else widget["default"]
#                 text_input_html += f"""
#                 <div class="widget input">
#                   <label for="{key}">{widget["label"]}</label><br>
#                   <textarea id="{key}" name="{key}" style="width:90%; height:60px; font-size:16px; padding:5px; box-sizing:border-box; resize:vertical;">{current_value}</textarea>
#                 </div>
#                 """
#             elif widget["type"] == "button":
#                 button_html += f"""
#                 <div class="widget button">
#                   <button type="submit" name="{key}" value="clicked">{widget["label"]}</button>
#                 </div>
#                 """

#         combined_html = f"""
#         <form method="POST">
#           {text_input_html}
#           <div class="button-container">
#             {button_html}
#           </div>
#         </form>
#         """
#         return combined_html

#     def home_page(self):
#         """Show stored content + chat history in chat bubbles."""
#         html_content = ""
#         for item in self.content_buffer:
#             html_content += f"<div>{item}</div>"

#         if has_request_context():
#             chat_history = session.get("chat_history", [])
#             if chat_history:
#                 for sender, message in chat_history:
#                     role_class = "user" if sender == "User" else "bot"
#                     html_content += f"<div class='chat-message {role_class}'><strong>{sender}:</strong> {message}</div>"
#         return html_content

#     def text_input(self, key, label, default=""):
#         """Register a text input widget."""
#         if key not in self.widgets:
#             self.widgets[key] = {"type": "text_input", "key": key, "label": label, "default": default}
#         # No immediate return, we rely on get_text_input_value to fetch it from session

#     def button(self, key, label, callback=None):
#         """Register a button widget."""
#         if key not in self.widgets:
#             self.widgets[key] = {"type": "button", "key": key, "label": label, "callback": callback}

#     def get_text_input_value(self, key, default=""):
#         """Get the current value from session for the given text input."""
#         if not has_request_context():
#             return default
#         return session.get(key, default)

#     def clear_text_input_value(self, key):
#         """Reset a text input field to empty string."""
#         if has_request_context():
#             session[key] = ""
#             session.modified = True

#     def get_chat_history(self):
#         """Return the chat history (list of (sender, message)) from session."""
#         if not has_request_context():
#             return []
#         return session.get("chat_history", [])

#     def set_chat_history(self, history):
#         """Set the chat history in session."""
#         if has_request_context():
#             session["chat_history"] = history
#             session.modified = True

#     def clear_chat_history(self):
#         """Clear chat history in session."""
#         if has_request_context():
#             session["chat_history"] = []
#             session.modified = True

#     def set_widget_position(self, position):
#         """Either 'top' or 'bottom'."""
#         if position not in ("top", "bottom"):
#             raise ValueError("Position must be 'top' or 'bottom'")
#         self.widget_position = position

#     def write(self, content):
#         """Append arbitrary HTML/string to the content buffer for the home page."""
#         self.content_buffer.append(str(content))

#     def run(self, host="127.0.0.1", port=5000):
#         """Run the Flask app."""
#         self.app.run(host=host, port=port)
