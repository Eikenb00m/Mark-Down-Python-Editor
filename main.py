import tkinter as tk
from tkinter import filedialog
import markdown
from tkinterweb import HtmlFrame

class MarkdownEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Markdown Editor with Live Preview")
        self.root.geometry("1200x600")

        # Create a Menu Bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Create a File menu and add Open and Save commands
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        menubar.add_cascade(label="File", menu=file_menu)

        # Create a PanedWindow to hold the editor and preview side by side
        self.paned_window = tk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=1)

        # Text editor on the left
        self.text_area = tk.Text(self.paned_window, wrap='word', font=("Arial", 12))
        self.paned_window.add(self.text_area)

        # HTML preview on the right using tkinterweb HtmlFrame
        self.preview_frame = HtmlFrame(self.paned_window)
        self.paned_window.add(self.preview_frame)

        # Toolbar
        toolbar = tk.Frame(self.root)
        toolbar.pack(side='top', fill='x')

        # Buttons for Markdown functionality
        buttons = [
            ("Bold", self.insert_bold), ("Italic", self.insert_italic), 
            ("Blockquote", self.insert_blockquote), ("H1", self.insert_heading1),
            ("H2", self.insert_heading2), ("H3", self.insert_heading3),
            ("Ordered List", self.insert_ordered_list), ("Unordered List", self.insert_unordered_list),
            ("Code", self.insert_inline_code), ("Horizontal Rule", self.insert_horizontal_rule),
            ("Link", self.insert_link), ("Image", self.insert_image),
            ("Table", self.insert_table), ("Strikethrough", self.insert_strikethrough),
            ("Task List", self.insert_task_list), ("Emoji", self.insert_emoji),
            ("Highlight", self.insert_highlight), ("Footnote", self.insert_footnote),
            ("Subscript", self.insert_subscript), ("Superscript", self.insert_superscript)
        ]

        for (text, command) in buttons:
            button = tk.Button(toolbar, text=text, command=command)
            button.pack(side='left')

        # Update preview when text changes
        self.text_area.bind("<<Modified>>", self.update_live_preview)

    def insert_bold(self):
        self.text_area.insert("insert", "**bold text**")

    def insert_italic(self):
        self.text_area.insert("insert", "*italicized text*")

    def insert_blockquote(self):
        self.text_area.insert("insert", "> blockquote")

    def insert_heading1(self):
        self.text_area.insert("insert", "# H1\n")

    def insert_heading2(self):
        self.text_area.insert("insert", "## H2\n")

    def insert_heading3(self):
        self.text_area.insert("insert", "### H3\n")

    def insert_ordered_list(self):
        self.text_area.insert("insert", "1. First item\n2. Second item\n3. Third item\n")

    def insert_unordered_list(self):
        self.text_area.insert("insert", "- First item\n- Second item\n- Third item\n")

    def insert_inline_code(self):
        self.text_area.insert("insert", "`code`")

    def insert_horizontal_rule(self):
        self.text_area.insert("insert", "---\n")

    def insert_link(self):
        self.text_area.insert("insert", "[title](https://www.example.com)")

    def insert_image(self):
        self.text_area.insert("insert", "![alt text](image.jpg)")

    def insert_table(self):
        self.text_area.insert("insert", "| Syntax | Description |\n| ----------- | ----------- |\n| Header | Title |\n| Paragraph | Text |\n")

    def insert_strikethrough(self):
        self.text_area.insert("insert", "~~The world is flat.~~")

    def insert_task_list(self):
        self.text_area.insert("insert", "- [x] Write the press release\n- [ ] Update the website\n- [ ] Contact the media\n")

    def insert_emoji(self):
        self.text_area.insert("insert", "That is so funny! :joy:")

    def insert_highlight(self):
        self.text_area.insert("insert", "I need to highlight these ==very important words==.")

    def insert_footnote(self):
        self.text_area.insert("insert", "Here's a sentence with a footnote. [^1]\n\n[^1]: This is the footnote.")

    def insert_subscript(self):
        self.text_area.insert("insert", "H~2~O")

    def insert_superscript(self):
        self.text_area.insert("insert", "X^2^")

    def update_live_preview(self, event):
        if self.text_area.edit_modified():  # Check if the text was modified
            content = self.text_area.get(1.0, 'end-1c')
            html_content = markdown.markdown(content)
            
            # Update preview window with rendered HTML
            self.preview_frame.load_html(html_content)

            self.text_area.edit_modified(False)  # Reset the modified flag

    def open_file(self):
        """Open a Markdown or text file and load its content into the editor."""
        file_path = filedialog.askopenfilename(filetypes=[("Markdown files", "*.md"), ("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.text_area.delete(1.0, tk.END)  # Clear current content
                self.text_area.insert(tk.END, content)  # Insert new content

    def save_file(self):
        """Save the current content of the editor to a Markdown file."""
        file_path = filedialog.asksaveasfilename(defaultextension=".md", filetypes=[("Markdown files", "*.md"), ("Text files", "*.txt")])
        if file_path:
            content = self.text_area.get(1.0, tk.END)  # Get content from editor
            with open(file_path, 'w') as file:
                file.write(content)  # Write content to the file

if __name__ == "__main__":
    root = tk.Tk()
    editor = MarkdownEditor(root)
    root.mainloop()
