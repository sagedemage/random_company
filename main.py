import random
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
import csv
import html
from pathlib import Path
import os

def read_csv(file_path: str) -> list:
    companies = []

    with open(file_path, "r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            companies.append(row)
    
    return companies


def create_us_companies_csv(read_file_path: str, write_file_path: str):
    companies = []
    fieldnames = []

    with open(read_file_path, "r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        fieldnames = reader.fieldnames
        for row in reader:
            if row["country"] == "United States":
                companies.append(row)

    with open(write_file_path, "w", newline='', encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for company_row in companies:
            writer.writerow(company_row)

class FilePath:
    def __init__(self, build_dir: str):
        self.dev = True
        self.build_dir = build_dir
        if Path.is_dir(self.build_dir):
            self.dev = False
    def get(self, file_path: str):
        if self.dev == False:
            file_path = os.path.join(self.build_dir, file_path)

        return file_path

class Theme:
    def __init__(self, bg, fg, font, padding):
        self.bg = bg
        self.fg = fg
        self.font = font
        self.padding = padding

class App(tk.Frame):
    def __init__(self, master: tk.Tk):
        width = 335
        height = 350
        master.title("Random Company")
        master.geometry(f"{width}x{height}")
        master.resizable(0, 0)

        bg_color = "#000000"
        fg_color = "#ffffff"
        font = ("Helvetica", 12)
        padding = 6
        theme = Theme(bg_color, fg_color, font, padding)
        master.config(bg=theme.bg)

        style = ThemedStyle(master, theme="breeze")
        style.configure(".", font=theme.font, foreground=theme.fg, background=theme.bg)

        super().__init__(master)
        self.pack()

        self.label = ttk.Label(text="Random Companies: ", font=theme.font)
        self.label.pack()
        self.company=tk.StringVar()

        self.list_box = tk.Listbox(height = 12, width = 35, bg=theme.bg, fg=theme.fg, font=theme.font)

        self.list_box.pack()

        button_1 = tk.Button(text="Generate", command=self.random_company, bg="#444444", fg=theme.fg, font=theme.font, padx=theme.padding, pady=theme.padding)
        button_1.pack()

        button_2 = tk.Button(text="Copy to clipboard", command=self.copy_to_clipboard, bg="#444444", fg=theme.fg, font=theme.font, padx=theme.padding, pady=theme.padding)
        button_2.pack()

        file_path = FilePath("_internal")

        read_csv_file = file_path.get("original_data/largest_companies_by_market_cap.csv")
        write_csv_file = file_path.get("data/largest_us_companies_by_market_cap.csv")

        check_write_file_path = Path(write_csv_file)
        if check_write_file_path.exists() == False:
            create_us_companies_csv(read_csv_file, write_csv_file)

        read_csv_file = file_path.get("data/largest_us_companies_by_market_cap.csv")

        self.companies = read_csv(read_csv_file)

        logo_path = file_path.get("images/logo.ico")

        master.iconbitmap(logo_path)
    
    def random_company(self):
        size = len(self.companies)

        indices = []
        for i in range(12):
            while True:
                index = random.randrange(0, size-1, 1)
                if index in indices:
                    continue
                else:
                    indices.append(index)
                    break

        self.list_box.delete(0,12)

        for i in range(len(indices)):
            index = indices[i]
            company_row = self.companies[index]
            company_name = html.unescape(company_row["Name"])
            self.list_box.insert(i+1, company_name)

    def copy_to_clipboard(self):
        self.clipboard_clear()
        index = self.list_box.curselection()
        if len(index) != 0:
            company = self.list_box.get(index)
            self.clipboard_append(company)

root = tk.Tk()
app = App(root)
app.mainloop()
