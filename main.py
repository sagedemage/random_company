import random
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
import csv

def read_csv(file_path: str) -> list:
    healthcare_companies = []

    with open(file_path) as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            healthcare_companies.append(row)
    
    return healthcare_companies

class App(tk.Frame):
    def __init__(self, master: tk.Tk):
        width = 300
        height = 150
        master.title("Random Company")
        master.geometry(f"{width}x{height}")
        master.resizable(0, 0)

        style = ThemedStyle(master, theme="breeze")

        style.configure("TButton", padding=6)
        style.configure("TEntry", padding=3)

        super().__init__(master)
        self.pack()

        self.label = ttk.Label(text="Company: ")
        self.label.pack()
        self.company=tk.StringVar()
        self.entry = ttk.Entry(textvariable=self.company, width=25)
        self.entry.pack()

        button_1 = ttk.Button(text="Random Company", command=self.random_company)
        button_1.pack()

        button_2 = ttk.Button(text="Copy to clipboard", command=self.copy_to_clipboard)
        button_2.pack()

        self.healthcare_companies = read_csv("data/healthcare_companies.csv")

        master.iconbitmap("images/logo.ico")
    
    def random_company(self):
        size = len(self.healthcare_companies)

        index = random.randrange(0, size-1, 1)
        company_row = self.healthcare_companies[index]

        self.company.set(company_row["Name"])

    def copy_to_clipboard(self):
        self.clipboard_clear()
        self.clipboard_append(self.company.get())

root = tk.Tk()
app = App(root)
app.mainloop()
