# syntaxmatrix/synta_mui.py
from flask import Flask, render_template_string, request, redirect, url_for, session, has_request_context
from collections import OrderedDict
from . import db

class SyntaxMUI:
    def __init__(self, title="SyntaxMUI App", nav_items=None, widget_position="top"):
        """
        Initialize the SyntaxMUI app.
        :param title: Title of the web app.
        :param nav_items: Dict mapping page names to functions returning HTML.
        :param widget_position: "top" or "bottom". If "bottom", widgets are fixed at the bottom.
        """
        self.app = Flask(__name__)
        self.app.secret_key = "syntaxmatrix_secret"  # For session state
        self.title = title
        self.nav_items = nav_items or {"Home": self.home_page}
        self.content_buffer = []  # For st.write() content
        self.widgets = OrderedDict()  # For widget definitions
        self.widget_position = widget_position  # "top" (default) or "bottom"
        self.setup_routes()

        db.init_db()
        persisted_pages = db.get_pages()
        for name, content in persisted_pages.items():
            if name != "Home":
                self.nav_items[name] = lambda content=content: content
        self.setup_routes()
    
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
                            background: #e0f7fa; /* Light blue background */
                            min-height: 80vh;
                            text-align: center;
                        }}
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
                        /* Text input styling */
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
        """Render the Home page with st.write() content and chat history."""
        html_content = "<h1>This is the Home Page</h1>"
        for item in self.content_buffer:
            html_content += f"<div>{item}</div>"
        
        if has_request_context():
            chat_history = session.get("chat_history", [])
            if chat_history:
                html_content += "<hr><h2>Chat History</h2>"
                for sender, message in chat_history:
                    html_content += f"<p><strong>{sender}:</strong> {message}</p>"
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

    def _get_text_input_value(self, key, default=""):
        return session.get(key, default)

    def _clear_text_input_value(self, key):
        session[key] = ""
        session.modified = True

    def _get_chat_history(self):
        return session.get("chat_history", [])

    def _set_chat_history(self, history):
        session["chat_history"] = history
        session.modified = True
    
    def run(self, host="127.0.0.1", port=5000):
        self.app.run(host=host, port=port)
    

# Global interface mimicking Streamlit.
_app_instance = SyntaxMUI()
write = _app_instance.write
run = _app_instance.run
text_input = _app_instance.text_input
button = _app_instance.button
set_widget_position = _app_instance.set_widget_position
clear_chat_history = _app_instance.clear_chat_history
