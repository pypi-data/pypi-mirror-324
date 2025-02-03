# syntaxmatrix/synta_mui.py
from flask import Flask, render_template_string, request, redirect, url_for, session, has_request_context, Response
from collections import OrderedDict
from . import db
import uuid, time

class SyntaxMUI:
    def __init__(self, title="SyntaxMUI App", nav_items=None, widget_position="top"):
        self.app = Flask(__name__)
        self.app.secret_key = "syntaxmatrix_secret"  # For session state
        self.title = title
        self.nav_items = nav_items or {"Home": self.home_page}
        self.content_buffer = []
        self.widgets = {}
        self.widget_position = widget_position
        self.setup_routes()

        db.init_db()
        persisted_pages = db.get_pages()
        for name, content in persisted_pages.items():
            if name != "Home":
                self.nav_items[name] = lambda content=content: content

        self._stream_data = {}    # stream_id -> dict of LLM info
        self._stream_results = {} # stream_id -> final text
        self.init_streaming_route()

        @self.app.route("/_syntaxmatrix_stream", methods=["POST"])
        def _one_global_stream_route():
            # This route can handle streaming for ANY request. 
            # You might read from session which user query to process, 
            # or pass an ID in request.form, etc.
            def generate():
                # yield partial tokens here
                ...
            return self.app.response_class(generate(), mimetype="text/plain")

    def init_streaming_route(self):
        """Define the /_syntaxmatrix_stream route exactly once, 
           so we never add routes after the first request."""
        @self.app.route("/_syntaxmatrix_stream", methods=["POST"])
        def _global_stream_handler():
            """
            Looks up a stream_id in form data, streams tokens from
            openai or any LLM, yields partial text.
            """
            form_data = request.form or {}
            stream_id = form_data.get("stream_id", "")
            if not stream_id or stream_id not in self._stream_data:
                return "Invalid or missing stream_id", 400

            # retrieve the data needed for streaming
            data = self._stream_data[stream_id]
            llm = data["llm"]
            model = data["model"]
            messages = data["messages"]
            temperature = data["temperature"]
            max_tokens = data["max_tokens"]
            extra_kwargs = data["extra_kwargs"]
            
            final_chunks = []

            def generate():
                try:
                    # Call the LLM with streaming
                    response = llm.chat.completions.create(
                        model=model,
                        messages=messages,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        stream=True,
                        **extra_kwargs
                    )
                    for chunk in response:
                        if ("choices" in chunk 
                            and chunk["choices"] 
                            and "delta" in chunk["choices"][0]
                            and "content" in chunk["choices"][0]["delta"]):
                            token_text = chunk["choices"][0]["delta"]["content"]
                            final_chunks.append(token_text)
                            yield token_text
                except Exception as e:
                    yield f"\n[stream_chat error: {e}]"
            
            # After streaming completes, store final text so stream_chat(...) can return it
            def finalize(_):
                self._stream_results[stream_id] = "".join(final_chunks)
                # Optionally remove from _stream_data if you don't need it anymore
                self._stream_data.pop(stream_id, None)

            resp = self.app.response_class(generate(), mimetype="text/plain")
            resp.call_on_close(lambda: finalize(None))
            return resp

    def stream_chat(self, llm, model, messages, temperature=0.7, max_tokens=150, **kwargs):
        """
        Create a unique stream_id, store the LLM data in _stream_data,
        inject JS that calls /_syntaxmatrix_stream, 
        and then wait for final text in _stream_results.
        """
        if not has_request_context():
            raise RuntimeError("stream_chat(...) must be called in a request context.")
        
        # 1) Generate a unique stream_id
        stream_id = uuid.uuid4().hex
        
        # 2) Store the data for the route to access
        self._stream_data[stream_id] = {
            "llm": llm,
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "extra_kwargs": kwargs,
        }
        self._stream_results[stream_id] = ""
        
        # 3) Inject a small JS snippet to call /_syntaxmatrix_stream w/ stream_id
        js_snippet = f"""
        <script>
        (function() {{
          var container = document.getElementById("chat-container");
          var botDiv = document.createElement("div");
          botDiv.className = "chat-message bot";
          botDiv.innerHTML = "<strong>Bot:</strong> ";
          container.appendChild(botDiv);
          
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
              reader.read().then(({ done, value } ) => {{
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
        self.write(js_snippet)

        # 4) Wait for final text in _stream_results 
        #    We'll do a simple poll-based approach, up to ~5s
        import time
        for _ in range(50):
            final_text = self._stream_results.get(stream_id, "")
            # If there's anything at all, assume it's complete 
            # once the route finishes
            if final_text:
                break
            time.sleep(0.1)
        
        return self._stream_results.pop(stream_id, "")

    @property
    def state(self):
        """
        A dictionary for storing session-specific state 
        (e.g. a 'messages' list for chat history).
        """
        # If there's no request context (e.g. code is run at import time),
        # just return an empty dictionary to avoid errors.
        if not has_request_context():
            return {}

        if "syntaxmatrix_state" not in session:
            session["syntaxmatrix_state"] = {}
        return session["syntaxmatrix_state"]

    def set_widget_position(self, position):
        """
        Change the widget position.
        :param position: "top" or "bottom"
        """
        if position not in ["top", "bottom"]:
            raise ValueError("Position must be 'top' or 'bottom'")
        self.widget_position = position

    def setup_routes(self):
        # Prevent duplicate registration if routes are already set up.
        if "index" in self.app.view_functions:
            return

        @self.app.route("/", methods=["GET", "POST"])
        def index():
            if request.method == "POST":
                # Process submitted widgets.
                for key, widget in self.widgets.items():
                    if widget["type"] == "text_input":
                        session[key] = request.form.get(key, widget["default"])
                    elif widget["type"] == "button":
                        if key in request.form and widget.get("callback"):
                            widget["callback"]()
                return redirect(url_for("index"))
            
            # Build the navigation menu.
            nav_html = "".join(f'<li><a href="/page/{item}">{item}</a></li>' for item in self.nav_items)
            nav_html += '<li><a href="/admin">Admin</a></li>'
            
            content = self.home_page()
            widget_form_html = self.render_widgets()
            
            # Auto-scroll script to scroll to the bottom.
            auto_scroll_script = """
            <script>
            window.onload = function() {
                window.scrollTo(0, document.body.scrollHeight);
            };
            </script>
            """
            
            if self.widget_position == "bottom":
                page_html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>{self.title}</title>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            margin: 0;
                            padding-bottom: 160px; /* Extra space for fixed widget container */
                            background: #f0f0f0;
                        }}
                        nav ul {{
                            list-style-type: none;
                            padding: 10px;
                            background: #333;
                        }}
                        nav li {{
                            display: inline;
                            margin-right: 15px;
                        }}
                        nav li a {{
                            color: #fff;
                            text-decoration: none;
                        }}
                        #chat-container {{
                            padding: 20px;
                            background: #f7f7f7;
                            min-height: 80vh;
                            max-width: 800px;
                            margin: 20px auto;
                            border-radius: 10px;
                            overflow-y: auto;
                        }}
                        /* Chat message bubble styling */
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
                            background-color: #dcf8c6;  /* Light green for user messages */
                            float: right;
                            text-align: right;
                        }}
                        .chat-message.bot {{
                            background-color: #ffffff;  /* White for bot messages */
                            float: left;
                            text-align: left;
                            border: 1px solid #ddd;
                        }}
                        /* Widget container remains fixed at the bottom */
                        #widget-container {{
                            position: fixed;
                            bottom: 0;
                            left: 0;
                            right: 0;
                            background: #f9f9f9;
                            border-top: 1px solid #ccc;
                            padding: 10px;
                            text-align: center;
                        }}
                        /* Multi-line text area styling for input */
                        .input textarea {{
                            width: 90%;
                            height: 60px;
                            font-size: 16px;
                            padding: 5px;
                            box-sizing: border-box;
                            resize: vertical;
                        }}
                        /* Horizontal button container */
                        .button-container {{
                            display: flex;
                            justify-content: center;
                            gap: 10px;
                            margin-top: 10px;
                        }}
                        .button-container button {{
                            font-size: 16px;
                            padding: 10px 20px;
                        }}
                    </style>
                                        
                </head>
                <body>
                    <nav>
                        <ul>{nav_html}</ul>
                    </nav>
                    <div id="chat-container">
                        {content}
                    </div>
                    <div id="widget-container">
                        {widget_form_html}
                    </div>
                    {auto_scroll_script}
                </body>
                </html>
                """
            else:
                page_html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>{self.title}</title>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                        }}
                        nav ul {{
                            list-style-type: none;
                            padding: 10px;
                            background: #333;
                        }}
                        nav li {{
                            display: inline;
                            margin-right: 15px;
                        }}
                        nav li a {{
                            color: #fff;
                            text-decoration: none;
                        }}
                        /* Text input styling */
                        .input textarea {{
                            width: 90%;
                            height: 60px;
                            font-size: 16px;
                            padding: 5px;
                            box-sizing: border-box;
                            resize: vertical;
                        }}
                        .button-container {{
                            display: flex;
                            justify-content: center;
                            gap: 10px;
                            margin-top: 10px;
                        }}
                        .button-container button {{
                            font-size: 16px;
                            padding: 10px 20px;
                        }}
                        #chat-container {{
                            padding: 20px;
                            background: #e0f7fa;
                            min-height: 80vh;
                            text-align: center;
                        }}
                    </style>
                </head>
                <body>
                    <nav>
                        <ul>{nav_html}</ul>
                    </nav>
                    <div>
                        {self.render_widgets()}
                    </div>
                    <div id="chat-container">
                        {content}
                    </div>
                    {auto_scroll_script}
                </body>
                </html>
                """
            return render_template_string(page_html)
            
        @self.app.route("/page/<page_name>")
        def page(page_name):
            if page_name in self.nav_items:
                return self.nav_items[page_name]()
            return "Page not found", 404

        @self.app.route("/admin", methods=["GET"])
        def admin_panel():
            pages_html = ""
            for page in self.nav_items:
                pages_html += f"""
                <tr>
                    <td>{page}</td>
                    <td>
                        <form action="/admin/update_page" method="POST" style="display:inline;">
                            <input type="hidden" name="old_page_name" value="{page}">
                            <input type="text" name="new_page_name" value="{page}">
                            <input type="submit" value="Update">
                        </form>
                    </td>
                </tr>
                """
            admin_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Admin Panel - {self.title}</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    table, th, td {{
                        border: 1px solid black;
                        border-collapse: collapse;
                        padding: 5px;
                    }}
                    th, td {{ text-align: left; }}
                    form {{ margin: 0; }}
                </style>
            </head>
            <body>
                <h1>Admin Panel</h1>
                <h2>Update Page Names</h2>
                <table>
                    <tr>
                        <th>Current Page Name</th>
                        <th>Update Page Name</th>
                    </tr>
                    {pages_html}
                </table>
                <h2>Add New Page</h2>
                <form action="/admin/add_page" method="POST">
                    <label for="page_name">Page Name:</label>
                    <input type="text" id="page_name" name="page_name" required>
                    <br><br>
                    <label for="page_content">Page Content (HTML):</label>
                    <br>
                    <textarea id="page_content" name="page_content" rows="5" cols="50" required></textarea>
                    <br><br>
                    <input type="submit" value="Add Page">
                </form>
                <br>
                <a href="/">Back to Home</a>
            </body>
            </html>
            """
            return admin_html

        @self.app.route("/admin/add_page", methods=["POST"])
        def add_page_ui():
            page_name = request.form.get("page_name")
            page_content = request.form.get("page_content")
            if page_name == "Home":
                return "Cannot add a page named 'Home'. <a href='/admin'>Back</a>"
            if page_name in self.nav_items:
                return f"Page '{page_name}' already exists. <a href='/admin'>Back</a>"
            try:
                db.add_page(page_name, page_content)
                # Add to nav_items using a lambda that captures the page content.
                self.nav_items[page_name] = lambda content=page_content: content
            except Exception as e:
                return str(e)
            return redirect(url_for("admin_panel"))

        @self.app.route("/admin/update_page", methods=["POST"])
        def update_page_ui():
            old_page_name = request.form.get("old_page_name")
            new_page_name = request.form.get("new_page_name")
            if old_page_name == "Home":
                return "Cannot update the 'Home' page via admin. <a href='/admin'>Back</a>"
            if not old_page_name or not new_page_name:
                return "Invalid input. <a href='/admin'>Back</a>"
            if old_page_name not in self.nav_items:
                return f"Page '{old_page_name}' not found. <a href='/admin'>Back</a>"
            # Get the current content by invoking the page function.
            current_content = self.nav_items[old_page_name]()
            try:
                db.update_page(old_page_name, new_page_name, current_content)
                # Update self.nav_items: remove the old key and add the new one.
                self.nav_items.pop(old_page_name)
                self.nav_items[new_page_name] = lambda content=current_content: content
            except Exception as e:
                return str(e) + " <a href='/admin'>Back</a>"
            return redirect(url_for("admin_panel"))

    def render_widgets(self):
        """Render text input and button widgets separately to group buttons horizontally."""
        if not self.widgets:
            return ""
        text_input_html = ""
        button_html = ""
        for key, widget in self.widgets.items():
            if widget["type"] == "text_input":
                current_value = session.get(key, widget["default"]) if has_request_context() else widget["default"]
                text_input_html += f"""
                <div class="widget input">
                    <label for="{key}">{widget["label"]}</label><br>
                    <textarea id="{key}" name="{key}" style="width:90%; height:60px; font-size:16px; padding:5px; box-sizing:border-box; resize:vertical;">{current_value}</textarea>
                </div>
                """
            elif widget["type"] == "button":
                button_html += f"""
                <div class="widget button">
                    <button type="submit" name="{key}" value="clicked">{widget["label"]}</button>
                </div>
                """
        combined_html = f"""
        <form method="POST">
        {text_input_html}
        <div class="button-container">
            {button_html}
        </div>
        </form>
        """
        return combined_html

    def home_page(self):
        """
        Render the Home page with a nicely formatted chat conversation.
        """
        html_content = "<h1>Welcome to SyntaxMatrix Chat</h1>"
        if has_request_context():
            chat_history = session.get("chat_history", [])
            if chat_history:
                html_content += "<div id='chat-messages'>"
                for sender, message in chat_history:
                    # Each message is wrapped in a div with classes "chat-message" and either "user" or "bot"
                    html_content += f"<div class='chat-message {sender.lower()}'><strong>{sender}:</strong> {message}</div>"
                html_content += "</div>"
        return html_content


    def add_page(self, page_name, content_function):
        if page_name in self.nav_items:
            raise ValueError(f"Page '{page_name}' already exists.")
        self.nav_items[page_name] = content_function

    def update_page(self, old_page_name, new_page_name):
        if old_page_name not in self.nav_items:
            raise ValueError(f"Page '{old_page_name}' does not exist.")
        if new_page_name in self.nav_items and new_page_name != old_page_name:
            raise ValueError(f"Page '{new_page_name}' already exists.")
        self.nav_items[new_page_name] = self.nav_items.pop(old_page_name)
    
    def write(self, content):
        self.content_buffer.append(str(content))
    
    def text_input(self, key, label, default=""):
        if key not in self.widgets:
            self.widgets[key] = {"type": "text_input", "key": key, "label": label, "default": default}
        return session.get(key, default) if has_request_context() else default
    
    def button(self, key, label, callback=None):
        if key not in self.widgets:
            self.widgets[key] = {"type": "button", "key": key, "label": label, "callback": callback}
        return False
    
    def clear_chat_history(self):
        if has_request_context():
            session["chat_history"] = []
            session.modified = True
    
    def get_text_input_value(self, key, default=""):
        """
        Return the current value of a text input from session state,
        or `default` if no value is set or outside a request context.
        """
        if not has_request_context():
            return default
        return session.get(key, default)

    def clear_text_input_value(self, key):
        session[key] = ""
        session.modified = True

    def get_chat_history(self):
        return session.get("chat_history", [])

    def set_chat_history(self, history):
        session["chat_history"] = history
        session.modified = True
    
    def stream_chat(self, llm, model, messages, temperature=0.7, max_tokens=150, **kwargs):
        """
        A high-level function that:
          1) Creates a one-time streaming route with a random URL.
          2) Injects a bit of JavaScript that fetches from that route and appends tokens to the UI.
          3) Waits behind the scenes for the stream to finish, then returns the final text.

        Developers only call st.stream_chat(...) from their callback code, 
        and see none of the route or JS details.
        """
        # 1) Generate a unique route name so we don't conflict if called multiple times
        route_id = f"/_syntaxmatrix_stream_{uuid.uuid4().hex}"

        # 2) We'll store the final text once streaming completes
        if not hasattr(self, "_stream_results"):
            self._stream_results = {}
        self._stream_results[route_id] = ""

        # 3) Define a route that yields partial tokens from the LLM
        @self.app.route(route_id, methods=["POST"])
        def _syntaxmatrix_stream_route():
            final_text_chunks = []

            def generate():
                try:
                    # Call the LLM with streaming
                    response = llm.chat.completions.create(
                        model=model,
                        messages=messages,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        stream=True,
                        **kwargs
                    )
                    for chunk in response:
                        if chunk.get("choices") and "delta" in chunk["choices"][0]:
                            delta = chunk["choices"][0]["delta"]
                            if "content" in delta:
                                token_text = delta["content"]
                                final_text_chunks.append(token_text)
                                yield token_text
                except Exception as e:
                    yield f"\n[stream_chat error: {e}]"

            # Build a streaming response
            r = self.app.response_class(generate(), mimetype="text/plain")

            # When the route closes, store the final text in self._stream_results
            def finalize(_):
                self._stream_results[route_id] = "".join(final_text_chunks)
            r.call_on_close(lambda: finalize(None))

            return r

        # 4) Inject a short snippet of JS that:
        #   - Creates a Bot bubble
        #   - fetches from the route
        #   - appends partial tokens as they arrive
        # We name the snippet uniquely to avoid collisions if multiple calls happen in the same request
        snippet_id = uuid.uuid4().hex
        js_snippet = f"""
        <script id="{snippet_id}">
        (function() {{
          // Create a new Bot bubble in the chat container
          var container = document.getElementById("chat-container");
          var botBubble = document.createElement("div");
          botBubble.className = "chat-message bot";
          botBubble.innerHTML = "<strong>Bot:</strong> ";
          container.appendChild(botBubble);

          // Now fetch partial tokens from "{route_id}"
          fetch("{route_id}", {{ method: "POST" }})
            .then(response => {{
              const reader = response.body.getReader();
              const decoder = new TextDecoder();
              function readChunk() {{
                reader.read().then(({{
                  done, value
                }}) => {{
                  if (done) return;
                  let chunk = decoder.decode(value);
                  botBubble.innerHTML += chunk;
                  window.scrollTo(0, document.body.scrollHeight);
                  readChunk();
                }});
              }}
              readChunk();
            }})
            .catch(err => {{
              console.error("SyntaxMatrix stream_chat error:", err);
              botBubble.innerHTML += "<br>[Error: " + err + "]";
            }});
        }})();
        </script>
        """
        # Insert that snippet into the page so it runs on the next render
        self.write(js_snippet)

        # 5) Wait (briefly) for the final text to appear in _stream_results
        #    We do a simple polling approach. A more robust approach might be SSE or websockets.
        for _ in range(50):  # up to ~5 seconds total
            final_text = self._stream_results.get(route_id, None)
            if final_text:
                # We have some final text
                break
            time.sleep(0.1)

        # Clear from _stream_results
        return self._stream_results.pop(route_id, "")
    
    def run(self, host="127.0.0.1", port=5000):
        """
        Runs the Flask application.
        """
        self.app.run(host=host, port=port)
