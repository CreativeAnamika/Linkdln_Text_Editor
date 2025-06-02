import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import json

# Unicode character mappings for different styles
BOLD_MAP = {
    'A': '𝗔', 'B': '𝗕', 'C': '𝗖', 'D': '𝗗', 'E': '𝗘', 'F': '𝗙', 'G': '𝗚', 'H': '𝗛', 'I': '𝗜',
    'J': '𝗝', 'K': '𝗞', 'L': '𝗟', 'M': '𝗠', 'N': '𝗡', 'O': '𝗢', 'P': '𝗣', 'Q': '𝗤', 'R': '𝗥',
    'S': '𝗦', 'T': '𝗧', 'U': '𝗨', 'V': '𝗩', 'W': '𝗪', 'X': '𝗫', 'Y': '𝗬', 'Z': '𝗭',
    'a': '𝗮', 'b': '𝗯', 'c': '𝗰', 'd': '𝗱', 'e': '𝗲', 'f': '𝗳', 'g': '𝗴', 'h': '𝗵', 'i': '𝗶',
    'j': '𝗷', 'k': '𝗸', 'l': '𝗹', 'm': '𝗺', 'n': '𝗻', 'o': '𝗼', 'p': '𝗽', 'q': '𝗾', 'r': '𝗿',
    's': '𝘀', 't': '𝘁', 'u': '𝘂', 'v': '𝘃', 'w': '𝘄', 'x': '𝘅', 'y': '𝘆', 'z': '𝘇',
    '0': '𝟬', '1': '𝟭', '2': '𝟮', '3': '𝟯', '4': '𝟰', '5': '𝟱', '6': '𝟲', '7': '𝟳', '8': '𝟴', '9': '𝟵'
}

ITALIC_MAP = {
    'A': '𝘈', 'B': '𝘉', 'C': '𝘊', 'D': '𝘋', 'E': '𝘌', 'F': '𝘍', 'G': '𝘎', 'H': '𝘏', 'I': '𝘐',
    'J': '𝘑', 'K': '𝘒', 'L': '𝘓', 'M': '𝘔', 'N': '𝘕', 'O': '𝘖', 'P': '𝘗', 'Q': '𝘘', 'R': '𝘙',
    'S': '𝘚', 'T': '𝘛', 'U': '𝘜', 'V': '𝘝', 'W': '𝘞', 'X': '𝘟', 'Y': '𝘠', 'Z': '𝘡',
    'a': '𝘢', 'b': '𝘣', 'c': '𝘤', 'd': '𝘥', 'e': '𝘦', 'f': '𝘧', 'g': '𝘨', 'h': '𝘩', 'i': '𝘪',
    'j': '𝘫', 'k': '𝘬', 'l': '𝘭', 'm': '𝘮', 'n': '𝘯', 'o': '𝘰', 'p': '𝘱', 'q': '𝘲', 'r': '𝘳',
    's': '𝘴', 't': '𝘵', 'u': '𝘶', 'v': '𝘷', 'w': '𝘸', 'x': '𝘹', 'y': '𝘺', 'z': '𝘻'
}



SCRIPT_MAP = {
    'A': '𝓐', 'B': '𝓑', 'C': '𝓒', 'D': '𝓓', 'E': '𝓔', 'F': '𝓕', 'G': '𝓖', 'H': '𝓗', 'I': '𝓘',
    'J': '𝓙', 'K': '𝓚', 'L': '𝓛', 'M': '𝓜', 'N': '𝓝', 'O': '𝓞', 'P': '𝓟', 'Q': '𝓠', 'R': '𝓡',
    'S': '𝓢', 'T': '𝓣', 'U': '𝓤', 'V': '𝓥', 'W': '𝓦', 'X': '𝓧', 'Y': '𝓨', 'Z': '𝓩',
    'a': '𝓪', 'b': '𝓫', 'c': '𝓬', 'd': '𝓭', 'e': '𝓮', 'f': '𝓯', 'g': '𝓰', 'h': '𝓱', 'i': '𝓲',
    'j': '𝓳', 'k': '𝓴', 'l': '𝓵', 'm': '𝓶', 'n': '𝓷', 'o': '𝓸', 'p': '𝓹', 'q': '𝓺', 'r': '𝓻',
    's': '𝓼', 't': '𝓽', 'u': '𝓾', 'v': '𝓿', 'w': '𝔀', 'x': '𝔁', 'y': '𝔂', 'z': '𝔃'
}

MONOSPACE_MAP = {
    'A': '𝙰', 'B': '𝙱', 'C': '𝙲', 'D': '𝙳', 'E': '𝙴', 'F': '𝙵', 'G': '𝙶', 'H': '𝙷', 'I': '𝙸',
    'J': '𝙹', 'K': '𝙺', 'L': '𝙻', 'M': '𝙼', 'N': '𝙽', 'O': '𝙾', 'P': '𝙿', 'Q': '𝚀', 'R': '𝚁',
    'S': '𝚂', 'T': '𝚃', 'U': '𝚄', 'V': '𝚅', 'W': '𝚆', 'X': '𝚇', 'Y': '𝚈', 'Z': '𝚉',
    'a': '𝚊', 'b': '𝚋', 'c': '𝚌', 'd': '𝚍', 'e': '𝚎', 'f': '𝚏', 'g': '𝚐', 'h': '𝚑', 'i': '𝚒',
    'j': '𝚓', 'k': '𝚔', 'l': '𝚕', 'm': '𝚖', 'n': '𝚗', 'o': '𝚘', 'p': '𝚙', 'q': '𝚚', 'r': '𝚛',
    's': '𝚜', 't': '𝚝', 'u': '𝚞', 'v': '𝚟', 'w': '𝚠', 'x': '𝚡', 'y': '𝚢', 'z': '𝚣',
    '0': '𝟶', '1': '𝟷', '2': '𝟸', '3': '𝟹', '4': '𝟺', '5': '𝟻', '6': '𝟼', '7': '𝟽', '8': '𝟾', '9': '𝟿'
}

SMALL_CAPS_MAP = {
    'a': 'ᴀ', 'b': 'ʙ', 'c': 'ᴄ', 'd': 'ᴅ', 'e': 'ᴇ', 'f': 'ғ', 'g': 'ɢ', 'h': 'ʜ', 'i': 'ɪ',
    'j': 'ᴊ', 'k': 'ᴋ', 'l': 'ʟ', 'm': 'ᴍ', 'n': 'ɴ', 'o': 'ᴏ', 'p': 'ᴘ', 'q': 'ǫ', 'r': 'ʀ',
    's': 's', 't': 'ᴛ', 'u': 'ᴜ', 'v': 'ᴠ', 'w': 'ᴡ', 'x': 'x', 'y': 'ʏ', 'z': 'ᴢ'
}

def transform_text(text, char_map):
    """Transform text using the provided character map"""
    return ''.join(char_map.get(c, c) for c in text)

def style_text(text, style):
    """Apply the specified style to the text"""
    if style == "bold":
        return transform_text(text, BOLD_MAP)
    elif style == "italic":
        return transform_text(text, ITALIC_MAP)
    elif style == "script":
        return transform_text(text, SCRIPT_MAP)
    elif style == "monospace":
        return transform_text(text, MONOSPACE_MAP)
    elif style == "smallcaps":
        return transform_text(text, SMALL_CAPS_MAP)
    else:
        return text

class LinkedInFormatterHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests to serve static files"""
        if self.path == "/":
            self.path = "/index.html"
        
        try:
            # Determine file path - files are in the static directory
            file_path = f"static{self.path}"
            file_ext = os.path.splitext(file_path)[1]
            
            # Set content type based on file extension
            content_type = {
                ".html": "text/html",
                ".css": "text/css",
                ".js": "application/javascript",
                ".png": "image/png",
                ".jpg": "image/jpeg",
                ".ico": "image/x-icon"
            }.get(file_ext, "text/plain")

            with open(file_path, "rb") as f:
                self.send_response(200)
                self.send_header("Content-type", content_type)
                self.end_headers()
                self.wfile.write(f.read())
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"File not found")

    def do_POST(self):
        """Handle POST requests to process text styling"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode("utf-8")
        
        # Parse form data or JSON
        if self.headers.get('Content-Type') == 'application/json':
            data = json.loads(post_data)
            text = data.get('text', '')
            style = data.get('style', 'normal')
        else:
            data = parse_qs(post_data)
            text = data.get('text', [''])[0]
            style = data.get('style', ['normal'])[0]

        # Apply the selected style
        styled_text = style_text(text, style)

        # Send response
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')  # Allow CORS
        self.end_headers()
        
        response = {'styled': styled_text}
        self.wfile.write(json.dumps(response).encode())

# Create the required directories
os.makedirs('static', exist_ok=True)

# Create index.html
with open('static/index.html', 'w', encoding='utf-8') as f:
    f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LinkedIn Text Formatter</title>
    <link rel="stylesheet" href="styles.css">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2905989940676776"
     crossorigin="anonymous"></script>
</head>
<body>
    <div class="container">
        <h1>LinkedIn Text Formatter</h1>
        <p class="description">Format your text to stand out on LinkedIn posts and messages.</p>
        
        <div class="editor-container">
  <textarea id="editor" placeholder="Write your post here..."></textarea>
  <div id="preview"></div>
</div>

        
            
            <div class="toolbar">
                <button onclick="applyStyle('bold')" class="btn">𝗕𝗼𝗹𝗱</button>
                <button onclick="applyStyle('italic')" class="btn">𝘐𝘵𝘢𝘭𝘪𝘤</button>
                <button onclick="applyStyle('script')" class="btn">𝓢𝓬𝓻𝓲𝓹𝓽</button>
                <button onclick="applyStyle('monospace')" class="btn">𝙼𝚘𝚗𝚘𝚜𝚙𝚊𝚌𝚎</button>
                <button onclick="applyStyle('smallcaps')" class="btn">sᴍᴀʟʟ ᴄᴀᴘs</button>
                <button onclick="clearText()" class="btn clear">Clear</button>
                <button onclick="copyText()" class="btn copy">Copy Text</button>
            </div>
        </div>
        
        
        
        <div class="instructions">
  <div class="instructions-block">
    <h3>How to use:</h3>
    <ol>
      <li>Type or paste your text in the editor</li>
      <li>Select the text you want to format</li>
      <li>Click on a style button</li>
      <li>Copy the formatted text and paste it into LinkedIn</li>
    </ol>
  </div>
  <p class="note">Note: This formatter uses Unicode characters that work in LinkedIn posts and messages.</p>
</div>


    

    
    <footer>
        <p>LinkedIn Text Formatter - Local Version</p>
    </footer>
    
    <script src="script.js"></script>
</body>
</html>""")

# Create styles.css
with open('static/styles.css', 'w', encoding='utf-8') as f:
    f.write("""* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #f5f5f5;
    padding: 20px;
}

.preview-container {
    margin-top: 30px;
    background-color: #f3f6f8;
    padding: 20px;
    border-radius: 4px;
}

#preview {
  width: 50%;
  height: 300px;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  overflow-y: auto;
  background-color: #f9f9f9;
}


.container {
    max-width: 800px;
    margin: 0 auto;
    background-color: #fff;
    padding: 30px;
    border-radius: 8px;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
}

h1 {
    text-align: center;
    color: #0077b5;  /* LinkedIn blue */
    margin-bottom: 10px;
}

.description {
    text-align: center;
    color: #666;
    margin-bottom: 25px;
}

.editor-container {
  display: flex;              /* Enables side-by-side layout */
  gap: 20px;                  /* Space between editor and preview */
  align-items: flex-start;   /* Align items at the top */
  margin-top: 20px;
}

#editor {
  width: 50%;
  height: 300px;
  padding: 10px;
  font-size: 16px;
  resize: vertical;
}

.toolbar {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

.btn {
    padding: 8px 16px;
    background-color: #f3f6f8;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.2s ease;
}

.btn:hover {
    background-color: #e1e9ee;
}

.copy {
    background-color: #0077b5;
    color: white;
    border: none;
}

.copy:hover {
    background-color: #005e93;
}

.clear {
    background-color: #f5f5f5;
}

.instructions {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 40px;
  text-align: center;
}

.instructions-block {
  display: flex;
  align-items: flex-start; /* Align h3 and list at the top */
  gap: 15px;
}

.instructions h3 {
  font-size: 20px;
  color: #0077b5;
  margin: 0;
  white-space: nowrap;
}

.instructions ol {
  margin: 0;
  padding-left: 20px;
  text-align: left;
}

.instructions li {
  font-size: 16px;
  line-height: 1.8;
  color: #444;
}

.instructions .note {
  font-size: 13px;
  color: #777;
  margin-top: 15px;
}


.note {
    font-size: 14px;
    color: #777;
    font-style: italic;
}

footer {
    margin-top: 30px;
    text-align: center;
    color: #777;
    font-size: 14px;
}

/* Toast notification */
.toast {
    visibility: hidden;
    min-width: 250px;
    background-color: #333;
    color: #fff;
    text-align: center;
    border-radius: 4px;
    padding: 16px;
    position: fixed;
    z-index: 1;
    bottom: 30px;
    left: 50%;
    transform: translateX(-50%);
    font-size: 14px;
}

.toast.show {
    visibility: visible;
    animation: fadein 0.5s, fadeout 0.5s 2.5s;
}

@keyframes fadein {
    from {bottom: 0; opacity: 0;}
    to {bottom: 30px; opacity: 1;}
}

@keyframes fadeout {
    from {bottom: 30px; opacity: 1;}
    to {bottom: 0; opacity: 0;}
}

@media (max-width: 600px) {
    .container {
        padding: 20px;
    }
    
    .toolbar {
        flex-direction: column;
    }
    
    .btn {
        width: 100%;
    }
}""")

# Create script.js
with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write("""const editor = document.getElementById('editor');

// Create toast element
const toast = document.createElement('div');
toast.className = 'toast';
document.body.appendChild(toast);

function showToast(message) {
    toast.textContent = message;
    toast.className = 'toast show';
    setTimeout(() => {
        toast.className = toast.className.replace('show', '');
    }, 3000);
}

function updatePreview(text) {
    const previewDiv = document.getElementById('preview');
    previewDiv.innerHTML = text;  // Allow HTML-like formatting
}

function applyStyle(style) {
    const start = editor.selectionStart;
    const end = editor.selectionEnd;

    if (start === end) {
        showToast('Please select some text first');
        return;
    }

    const selectedText = editor.value.substring(start, end);

    fetch('/style', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            text: selectedText,
            style: style
        })
    })
    .then(response => response.json())
    .then(data => {
        // Combine the full text with the styled selection
        const newText = editor.value.substring(0, start) + data.styled + editor.value.substring(end);
        editor.value = newText;

        // Set cursor back to where user left off
        editor.selectionStart = start;
        editor.selectionEnd = start + data.styled.length;
        editor.focus();

        // ✅ NOW: Preview entire updated content
        updatePreview(newText);  // Instead of data.styled
    })
    .catch(error => {
        console.error('Error styling text:', error);
        showToast('Error applying style');
    });
}



function clearText() {
    editor.value = '';
    editor.focus();
}

function copyText() {
    if (editor.value.trim() === '') {
        showToast('Nothing to copy');
        return;
    }
    
    editor.select();
    document.execCommand('copy');
    
    // Restore selection
    editor.selectionEnd = editor.selectionStart;
    
    showToast('Text copied to clipboard!');
}

// Add keyboard shortcuts
// Listen for text changes and update preview
editor.addEventListener('input', function() {
    updatePreview(editor.value);
});


editor.addEventListener('keydown', function(e) {
    // Ctrl+B for bold
    if (e.ctrlKey && e.key === 'b') {
        e.preventDefault();
        applyStyle('bold');
    }
    
    // Ctrl+I for italic
    if (e.ctrlKey && e.key === 'i') {
        e.preventDefault();
        applyStyle('italic');
    }
});""")

def main():
    # Create and start the server
    server_address = ('', 8000)  # Host on all interfaces, port 8000
    httpd = HTTPServer(server_address, LinkedInFormatterHandler)
    print("✅ Server started at http://localhost:8000")
    httpd.serve_forever()

if __name__ == "__main__":
    main()