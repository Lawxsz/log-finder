# github.com/lawxsz t.me/lawxsz credits!!

import subprocess
import sys

def install_modules(modules):
    for module in modules:
        try:
            __import__(module)
        except ImportError:
            print(f"The module '{module}' is not installed. Installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", module])

required_modules = ["customtkinter", "tkfontawesome", "colorama"]

install_modules(required_modules)

import os
from datetime import datetime
import customtkinter as ctk
from tkinter import filedialog, StringVar, END
import threading
from colorama import init, Fore

init(autoreset=True)

search_cancelled = False
search_in_progress = False
files_to_search = []
current_file_index = 0

def save_results(page, results, console_textbox):
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    file_name = f"{page}_{timestamp}.txt"
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write("=== t.me/lawxszchannel ===\n")
        for result in results:
            parts = result.split(':')
            if len(parts) >= 2:
                url = parts[0].strip()
                user_password = ':'.join(parts[1:]).strip()

                if url.startswith('http://') or url.startswith('https://'):
                    if ':' in user_password:
                        username, password = user_password.split(':', 1)

                        file.write("===================\n")
                        file.write(f"Url: {url}\n")
                        file.write(f"Username: {username}\n")
                        file.write(f"Password: {password}\n")
                        file.write("===================\n\n")
                    else:
                        file.write(f"Invalid format: {result}\n")
                        file.write("===================\n\n")
                else:
                    file.write(f"Invalid URL format: {url}\n")
                    file.write("===================\n\n")
            else:
                file.write(f"Invalid format: {result}\n")
                file.write("===================\n\n")
    
    console_textbox.insert(END, f"Results saved in: {file_name}\n")

def extract_page(url):
    if "://" in url:
        url = url.split('://')[1]
    return url.split('/')[0]

def search_in_file(file, search_term, console_textbox, found_accounts_label, progressbar):
    global search_cancelled, search_in_progress
    results = []
    found_accounts = 0

    try:
        with open(file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            total_lines = len(lines)
            for i, line in enumerate(lines):
                if search_cancelled:
                    console_textbox.insert(END, "Search cancelled.\n")
                    break

                if search_term in line:
                    results.append(line.strip())
                    found_accounts += 1
                    console_textbox.insert(END, f"{line.strip()}\n")

                progress = (i + 1) / total_lines * 100
                progressbar.set(progress)

        if not search_cancelled:
            if results:
                first_match = extract_page(results[0].split(':')[0])
                save_results(first_match, results, console_textbox)
                found_accounts_label.set(f"Accounts found: {found_accounts}")
            else:
                console_textbox.insert(END, f"No results found for the term: {search_term}\n")
    except Exception as e:
        console_textbox.insert(END, f"Error: {str(e)}\n")
    finally:
        progressbar.set(0)
        search_in_progress = False

def load_files(file_entry):
    global files_to_search
    files = filedialog.askopenfilenames(filetypes=[("Text files", "*.txt")])
    files_to_search = files
    file_entry.set(", ".join(files))

def start_search(file_entry, search_term_entry, console_textbox, found_accounts_label, progressbar):
    global search_cancelled, search_in_progress, current_file_index
    search_cancelled = False
    search_in_progress = True

    console_textbox.delete('1.0', END)
    
    if not files_to_search:
        console_textbox.insert(END, "No files selected.\n")
        return

    if current_file_index < len(files_to_search):
        file = files_to_search[current_file_index]
        search_term = search_term_entry.get()
        if not os.path.exists(file):
            console_textbox.insert(END, f"The file {file} does not exist.\n")
        elif not search_term:
            console_textbox.insert(END, "You must enter a search term.\n")
        else:
            threading.Thread(target=search_in_file, args=(file, search_term, console_textbox, found_accounts_label, progressbar)).start()
    else:
        console_textbox.insert(END, "All files have been processed.\n")

def pause_search():
    global search_in_progress
    if search_in_progress:
        console_textbox.insert(END, "Search paused. Press 'Resume' to continue.\n")
        global search_cancelled
        search_cancelled = True
        search_in_progress = False

def resume_search(file_entry, search_term_entry, console_textbox, found_accounts_label, progressbar):
    global search_in_progress, current_file_index
    if not search_in_progress and current_file_index < len(files_to_search):
        current_file_index += 1
        start_search(file_entry, search_term_entry, console_textbox, found_accounts_label, progressbar)

def create_panel():
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Combo Search Panel - Made by @lawxsz")

    file_entry = StringVar()
    search_term_entry = StringVar()
    found_accounts_label = StringVar(value="Accounts found: 0")

    root.geometry("900x700")

    bg_color = "#f1f1f1"
    button_color = "#3b82f6"
    pause_color = "#ff4c4c"
    text_color = "#000000"
    highlight_color = "#d1d5db"

    root.configure(bg=bg_color)

    file_label = ctk.CTkLabel(root, text="Select combo files", fg_color=bg_color, text_color=text_color, font=("Arial", 16, "bold"))
    file_label.pack(pady=10)

    file_input = ctk.CTkEntry(root, textvariable=file_entry, width=600, height=30, corner_radius=8, border_color=highlight_color, border_width=2)
    file_input.pack(pady=5)

    file_button = ctk.CTkButton(root, text="Load files", command=lambda: load_files(file_entry), fg_color=button_color, corner_radius=8)
    file_button.pack(pady=5)

    search_term_label = ctk.CTkLabel(root, text="Enter search term", fg_color=bg_color, text_color=text_color, font=("Arial", 16, "bold"))
    search_term_label.pack(pady=10)

    search_term_input = ctk.CTkEntry(root, textvariable=search_term_entry, width=600, height=30, corner_radius=8, border_color=highlight_color, border_width=2)
    search_term_input.pack(pady=5)

    control_frame = ctk.CTkFrame(root, fg_color=bg_color)
    control_frame.pack(pady=20)

    search_button = ctk.CTkButton(control_frame, text="Start Search", command=lambda: start_search(file_entry, search_term_entry, console_textbox, found_accounts_label, progressbar), fg_color=button_color, corner_radius=8)
    search_button.pack(side="left", padx=5)

    pause_button = ctk.CTkButton(control_frame, text="Pause", command=pause_search, fg_color=pause_color, corner_radius=8)
    pause_button.pack(side="left", padx=5)

    resume_button = ctk.CTkButton(control_frame, text="Resume", command=lambda: resume_search(file_entry, search_term_entry, console_textbox, found_accounts_label, progressbar), fg_color=button_color, corner_radius=8)
    resume_button.pack(side="left", padx=5)

    accounts_label = ctk.CTkLabel(root, textvariable=found_accounts_label, fg_color=bg_color, text_color=text_color, font=("Arial", 14))
    accounts_label.pack(pady=10)

    console_textbox = ctk.CTkTextbox(root, width=600, height=200, corner_radius=8)
    console_textbox.pack(pady=10)

    progressbar = ctk.CTkProgressBar(root, width=600)
    progressbar.pack(pady=10)

    credits_label = ctk.CTkLabel(root, text="Developed by @lawxsz", fg_color=bg_color, text_color=text_color, font=("Arial", 12, "italic"))
    credits_label.pack(pady=5)

    root.mainloop()

create_panel()
