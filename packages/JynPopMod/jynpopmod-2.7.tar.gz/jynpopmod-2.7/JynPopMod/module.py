"""
What Users Can Do:
1. **Use for Personal and Non-Commercial Purposes:**  
   Users can download and use the Software for personal projects, non-commercial projects, or educational purposes, as long as it's not for profit or commercial gain.

2. **Incorporate into Larger Projects:**  
   Users can include the Software in larger projects, either public or private, but **with proper attribution** (e.g., crediting the original author, "Jynoqtra").

3. **Modify for Personal Use:**  
   Users can modify the Software for their own use within a larger project, as long as any modifications are clearly documented (e.g., note which parts were changed).

4. **Publicly Distribute:**  
   Users can distribute their projects that use the Software publicly, but **U must provide proper attribution** to the original author and include the required notice ("This project includes software developed by [Jynoqtra], © 2025...").

---

### **What Users Can't Do:**
1. **Commercial Use Without Permission:**  
   Users cannot use the Software for commercial purposes (e.g., selling it, using it in a product sold for profit) without any **consent** from the Licensor.

2. **Resell or Sublicense the Software:**  
   Users cannot sell, lease, or sublicense the Software as a standalone product. The Software cannot be distributed as-is for a fee or bundled with another product for resale.

3. **Alter or Copy the Original Software (or parts of it) Without Permission:**  
   Users cannot modify the core form of the Software and then redistribute it as part of their project, unless U clearly state any changes made. Copying portions of the Software for redistribution or use in other projects **without the necessary modifications** is prohibited.

4. **Failing to Give Proper Attribution:**  
   If a user integrates the Software into any project that is shared or published, U must ensure the correct **attribution** notice is visible and readable, as specified in the agreement.

---

### **How U Can Use the Software:**
**1. Permission for Commercial Use or Profit**  
If you want to use the Software for **commercial purposes** (e.g., selling a product that includes it or using it in a business), you **must get permission** from the Licensor.  

Alternatively, you can use the Software commercially **without prior permission** if you **credit "Jynoqtra" properly** by:  
- Displaying the **Jynoqtra logo** in your commercial content.  
- Ensuring the logo appears **clearly** in the video for **at least 3 seconds** in **HD quality** and is **easily visible** (not hidden or covered).  

© 2025 [Jynoqtra]
"""

"Want an useless ice cream button that doesn't work at all?"
"click this:  https://jynoqtra.weebly.com/ice-cream.html "



from http.server import SimpleHTTPRequestHandler, HTTPServer
import socketserver
import logging
import socket
import http
import json
import shutil
import subprocess
import os
import time
import random
import uuid
import socket
import inspect
import smtplib
from email.message import EmailMessage
import threading
import sys

#  FTing
import requests
#  FTing

def wait(key="s", num=1):
    if key.lower() == "s":
        time.sleep(num)
    elif key.lower() == "m":
        time.sleep(num * 60)
    elif key.lower() == "h":
        time.sleep(num * 3600)
    else:
        print("Error: Use 's' for seconds, 'm' for minutes, or 'h' for hours.")

def ifnull(_v, _d):
    return _d if _v is None or _v == "" else _v

def switch_case(_v, _c, d=None):
    action = _c.get(_v, d)
    return action() if callable(action) else action

def timer_function(func, seconds):
    time.sleep(seconds)
    func()

def iftrue(var, function):
    if var:
        function()

def iffalse(var, function):
    if not var:
        function()
        
def isequal(text,atext):
    if text.lower() == atext:return True
    else:return False

def replace(string, replacement, replacement_with):
    return string.replace(replacement, replacement_with)

def until(function, whattodo):
    function()
    while True:
        whattodo()
        if function():break

def repeat(function, times):
    for _ in range(times):
        function()

def oncondit(condition, function_true, function_false):
    if condition:
        function_true()
    else:
        function_false()

def repeat_forever(function):
    while True:
        function()

def safe_run(func, *args, **kwargs):
    try:
        func(*args, **kwargs)
    except Exception as e:
        print(f"Error occurred in function {func.__name__}: {e}")
        return None

def start_timer(seconds, callback):
    time.sleep(seconds)
    callback()

def generate_random_string(length=15):
    characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@/-*_'
    return ''.join(random.choices(characters, k=length))

def get_ip_address():
    return socket.gethostbyname(socket.gethostname())

def send_email(subject, body, to_email, mailname, mailpass):
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = mailname
    msg["To"] = to_email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(mailname, mailpass)
            server.send_message(msg)
            print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

def generate_unique_id():
    return str(uuid.uuid4())

def start_background_task(backtask):
    thread = threading.Thread(target=backtask)
    thread.start()

def nocrash(func):
    def wrapper(*args, **kwargs):
        return safe_run(func, *args, **kwargs)
    return wrapper

def parallel(*functions):
    threads = []
    for func in functions:
        thread = threading.Thread(target=func)
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

def gs(func):
    return inspect.getsource(func)

def Jctb(input_string):
    def char_to_binary(c):
        if c == ' ':
            return '0000000001'
        elif c == '\n':
            return '0000000010'
        alphabet_upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        alphabet_lower = 'abcdefghijklmnopqrstuvwxyz'
        if c in alphabet_upper:
            return format(alphabet_upper.index(c), '010b')
        elif c in alphabet_lower:
            return format(alphabet_lower.index(c) + 26, '010b')
        return None

    binary_string = ''.join(char_to_binary(char) for char in input_string if char_to_binary(char))
    return binary_string


def Jbtc(binary_input):
    def binary_to_char(binary_vector):
        if binary_vector == '0000000001':
            return ' '
        elif binary_vector == '0000000010':
            return '\n'
        alphabet_upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        alphabet_lower = 'abcdefghijklmnopqrstuvwxyz'
        num = int(binary_vector, 2)
        if 0 <= num <= 25:
            return alphabet_upper[num]
        elif 26 <= num <= 51:
            return alphabet_lower[num - 26]
        return None

    char_list = [binary_to_char(binary_input[i:i+10]) for i in range(0, len(binary_input), 10)]
    return ''.join(char_list)

import tkinter as tk
class Jwin:
    def __init__(self, layout, widgets_config, user_callbacks=None):
        self.root = tk.Tk()
        self.root.title("Dynamic Window")
        self.widgets = {}
        self.user_callbacks = user_callbacks or {}
        self.layout_lines = [line.strip() for line in layout.strip().split("\n") if line.strip()]
        self.num_rows = len(self.layout_lines)
        self.num_cols = max(len(line) for line in self.layout_lines)
        for r in range(self.num_rows):
            self.root.grid_rowconfigure(r, weight=1)
        for c in range(self.num_cols):
            self.root.grid_columnconfigure(c, weight=1)
        self._create_widgets(widgets_config)
        self._create_layout()

    def _create_widgets(self, widgets_config):
        for widget_config in widgets_config:
            row, col = widget_config['position']
            widget_type = widget_config['type']
            options = widget_config.get('options', {})
            widget = self._create_widget(widget_type, options)
            if widget:
                widget.grid(row=row, column=col, padx=5, pady=5)
                widget_id = options.get("id")
                if widget_id:
                    self.widgets[widget_id] = widget

    def _create_widget(self, widget_type, options):
        if widget_type == "button":
            return tk.Button(self.root, text=options.get("text", "Button"),
                             command=lambda: self._execute_callback(options.get("id")))
        elif widget_type == "label":
            return tk.Label(self.root, text=options.get("text", "Label"))
        elif widget_type == "input":
            return tk.Entry(self.root)
        elif widget_type == "password":
            return tk.Entry(self.root, show="*")
        elif widget_type == "checkbox":
            return tk.Checkbutton(self.root, text=options.get("text", "Checkbox"))
        elif widget_type == "textarea":
            return tk.Text(self.root, height=5, width=20)
        else:
            return tk.Label(self.root, text=f"Unsupported: {widget_type}")

    def _create_layout(self):
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                if self.layout_lines[r][c] == " ":
                    continue

    def _execute_callback(self, widget_id):
        if widget_id and widget_id in self.user_callbacks:
            callback = self.user_callbacks[widget_id]
            if callable(callback):
                callback()

    def run(self):
        self.root.mainloop()


    def show_error_messagebox(message):
        root = tk.Tk()
        root.withdraw()
        tk.messagebox.showerror("Error", message)


def encode_base64(data):
    base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    binary_data = ''.join([f"{ord(c):08b}" for c in data])
    padding = len(binary_data) % 6
    if padding != 0:
        binary_data += '0' * (6 - padding)
    encoded = ''.join([base64_chars[int(binary_data[i:i+6], 2)] for i in range(0, len(binary_data), 6)])
    encoded += "=" * ((4 - len(encoded) % 4) % 4)
    print(f"Base64: {encoded}")
    return encoded

def decode_base64(encoded_data):
    base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    encoded_data = encoded_data.rstrip("=")
    binary_data = ''.join([f"{base64_chars.index(c):06b}" for c in encoded_data])
    decoded = ''.join([chr(int(binary_data[i:i+8], 2)) for i in range(0, len(binary_data), 8)])
    print(f"Decoded: {decoded}")
    return decoded

def reverse_string(string):
    return string[::-1]

def calculate_factorial(number):
    if number == 0:
        return 1
    return number * calculate_factorial(number - 1)

def generate_random_string(length=15):
    charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@/-*_'
    random_string = ''
    for _ in range(length):
        random_string += charset[calculate_factorial(len(charset)) % len(charset)]
    return random_string

def swap_values(a, b):
    return b, a

def replace(string, old, new):
    result = ''
    for char in string:
        if char == old:
            result += new
        else:
            result += char
    return result

def find_maximum(numbers):
    max_val = numbers[0]
    for num in numbers:
        if num > max_val:
            max_val = num
    return max_val

def find_minimum(numbers):
    min_val = numbers[0]
    for num in numbers:
        if num < min_val:
            min_val = num
    return min_val

def sum_list(lst):
    total = 0
    for num in lst:
        total += num
    return total

def reverse_list(lst):
    return lst[::-1]

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def split_into_chunks(text, chunk_size):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def unique_elements(lst):
    unique_lst = []
    for item in lst:
        if item not in unique_lst:
            unique_lst.append(item)
    return unique_lst

def calculate_average(numbers):
    if not numbers:
        return 0
    return sum_list(numbers) / len(numbers)

def calculate_median(numbers):
    sorted_numbers = sorted(numbers)
    n = len(sorted_numbers)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_numbers[mid - 1] + sorted_numbers[mid]) / 2
    return sorted_numbers[mid]

def count_words(text):
    return len(text.split())

def count_sentences(text):
    sentences = text.split('.')
    return len([s for s in sentences if s.strip()])

def add_commas(input_string):
    return ','.join(input_string)

def remove_spaces(text):
    return ''.join([char for char in text if char != ' '])

def calculate_square_root(number):
    if number < 0:
        return None
    guess = number / 2.0
    for _ in range(20):
        guess = (guess + number / guess) / 2.0
    return guess

def find_files_by_extension(directory, extension):
    return [f for f in os.listdir(directory) if f.endswith(extension)]

def get_curr_dir():
    return os.getcwd()

def check_if_file_exists(file_path):
    return os.path.exists(file_path)

def monitor_new_files(directory, callback):
    known_files = set(os.listdir(directory))
    while True:
        current_files = set(os.listdir(directory))
        new_files = current_files - known_files
        if new_files:
            callback(new_files)
        known_files = current_files
        time.sleep(1)


def monitor_file_changes(file_path, callback):
    last_modified = os.path.getmtime(file_path)
    while True:
        current_modified = os.path.getmtime(file_path)
        if current_modified != last_modified:
            last_modified = current_modified
            callback()
        time.sleep(1)

def write_to_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)

def read_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

def parse_json(json_string):
    return json.loads(json_string)

def create_file_if_not_exists(filename):
    if not os.path.exists(filename):
        with open(filename, 'w') as file:
            file.write('')

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def create_zip_file(source_dir, output_zip):
    shutil.make_archive(output_zip, 'zip', source_dir)

def extract_zip_file(zip_file, extract_dir):
    shutil.unpack_archive(zip_file, extract_dir)

def move_file(source, destination):
    shutil.move(source, destination)

def copy_file(source, destination):
    shutil.copy(source, destination)

def show_file_properties(file_path):
    stats = os.stat(file_path)
    return f"Size: {stats.st_size} bytes, Last Modified: {time.ctime(stats.st_mtime)}"


def start_http_server(ip="0.0.0.0", port=8000):
    server_address = (ip, port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"Server started on {ip}:{port}")
    httpd.serve_forever()

def stop_http_server():
    print("Stopping server...")
    exit(0)

def get_server_status(url="http://localhost:8000"):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("Server is up and running.")
        else:
            print(f"Server is down. Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to server: {e}")

def set_server_timeout(timeout=10):
    socket.setdefaulttimeout(timeout)
    print(f"Server connection timeout set to {timeout} seconds.")

def upload_file_to_server(file_path, url="http://localhost:8000/upload"):
    with open(file_path, 'rb') as file:
        response = requests.post(url, files={'file': file})
        if response.status_code == 200:
            print(f"File successfully uploaded: {file_path}")
        else:
            print(f"File upload failed. Status Code: {response.status_code}")

def download_file_from_server(file_url, save_path):
    response = requests.get(file_url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"File downloaded: {save_path}")
    else:
        print(f"File download failed. Status Code: {response.status_code}")

class CustomRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Welcome! Server is running.")
        elif self.path == "/status":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status": "online"}')
        else:
            self.send_response(404)
            self.end_headers()

def start_custom_http_server(ip="0.0.0.0", port=8000):
    server_address = (ip, port)
    httpd = HTTPServer(server_address, CustomRequestHandler)
    print(f"Custom server started on {ip}:{port}")
    httpd.serve_forever()

def set_server_access_logs(log_file="server_access.log"):
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')
    print(f"Access logs are being saved to {log_file}")

def get_server_logs(log_file="server_access.log"):
    try:
        with open(log_file, 'r') as log:
            logs = log.readlines()
            print("".join(logs))
    except FileNotFoundError:
        print(f"{log_file} not found.")

def restart_http_server():
    print("Restarting server...")
    os.execv(sys.executable, ['python'] + sys.argv)

def check_internet_connection():
    response = os.system("ping -c 1 google.com")
    return response == 0

def create_web_server(directory, port=8000):
    os.chdir(directory)
    handler = SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Serving {directory} at http://localhost:{port}")
        httpd.serve_forever()

def create_custom_web_server(html, port=8000):
    html_content = html

    class CustomHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))

    with socketserver.TCPServer(("", port), CustomHandler) as httpd:
        print(f"Serving custom HTML page at http://0.0.0.0:{port}")
        print("Anyone on the same network can access this. (if not work use this http://127.0.0.1:8000)")
        httpd.serve_forever()
def JynParser(rep):
    inj= """
    global main
    main = rep
    """
    exec()

def contains(input, str):
    return str in input

def Jusbcam(Device_Name):
    try:
        result = subprocess.run(
            ['wmic', 'path', 'Win32_PnPEntity', 'where', 'DeviceID like "USB%"', 'get', 'Name'],
            capture_output=True, text=True, encoding="utf-8", errors="ignore"
        )
        if result.stdout:
            output = result.stdout.strip().split("\n")[1:]
            devices = [line.strip() for line in output if line.strip()]
            return contains(devices,Device_Name)
        else:
            return []
    except Exception as e:
        print(f"Error detecting devices: {e}")
        return []
