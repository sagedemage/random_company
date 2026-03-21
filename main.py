import random
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
import csv
import html

def read_csv(file_path: str) -> list:
    companies = []

    with open(file_path, "r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            companies.append(row)
    
    return companies

class App(tk.Frame):
    def __init__(self, master: tk.Tk):
        width = 335
        height = 350
        master.title("Random Company")
        master.geometry(f"{width}x{height}")
        master.resizable(0, 0)

        style = ThemedStyle(master, theme="breeze")

        style.configure("TButton", padding=6)
        style.configure("TEntry", padding=3)
        style.configure(".", font=("Helvetica", 12))

        super().__init__(master)
        self.pack()

        self.label = ttk.Label(text="Random Companies: ", font=("Helvetica", 12))
        self.label.pack()
        self.company=tk.StringVar()

        self.list_box = tk.Listbox(height = 12, width = 35, bg="#ffffff", font=("Helvetica", 12))

        self.list_box.pack()

        button_1 = ttk.Button(text="Generate", command=self.random_company)
        button_1.pack()

        button_2 = ttk.Button(text="Copy to clipboard", command=self.copy_to_clipboard)
        button_2.pack()

        self.companies = read_csv("data/largest_companies_by_market_cap.csv")

        master.iconbitmap("images/logo.ico")
    
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
