import random
import csv
import html
from pathlib import Path
import os
import wx

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

class WxApp(wx.Frame):
    def __init__(self, *args, **kw):
        super(WxApp, self).__init__(*args, **kw)

        window_width = 300
        window_height = 350
        window_size = wx.Size(window_width, window_height)
        self.SetSize(window_size)
        frame_style = (wx.SYSTEM_MENU |
                       wx.MINIMIZE_BOX |
                       wx.MAXIMIZE_BOX |
                       wx.CLOSE_BOX |
                       wx.CAPTION |
                       wx.CLIP_CHILDREN)

        self.SetWindowStyleFlag(frame_style)

        panel = wx.Panel(self)

        text = wx.StaticText(panel, label="Random Companies: ")

        list_box_width = 200
        list_box_height = 190
        list_box_size = wx.Size(list_box_width, list_box_height)
        self.list_box = wx.ListBox(panel, size=list_box_size)

        generate_button = wx.Button(panel, label="Generate", size=wx.DefaultSize)
        copy_to_clipboard_button = wx.Button(panel, label="Copy to Clipboard", size=wx.DefaultSize)

        box_sizer = wx.BoxSizer(wx.VERTICAL)
        box_sizer.Add(text, 0, wx.ALIGN_CENTER_HORIZONTAL, 10)
        box_sizer.Add(self.list_box, 0, wx.ALIGN_CENTER_HORIZONTAL, 10)
        box_sizer.Add(generate_button, 0, wx.ALIGN_CENTER_HORIZONTAL, 10)
        box_sizer.Add(copy_to_clipboard_button, 0, wx.ALIGN_CENTER_HORIZONTAL, 10)
        panel.SetSizer(box_sizer)

        file_menu = wx.Menu()
        hello_item = file_menu.Append(-1, "&Hello...\tCtrl-H", "Help string shown in status bar for this menu item")
        file_menu.AppendSeparator()
        exit_item = file_menu.Append(wx.ID_EXIT)
        help_menu = wx.Menu()
        about_item = help_menu.Append(wx.ID_ABOUT)

        menu_bar = wx.MenuBar()
        menu_bar.Append(file_menu, "&File")
        menu_bar.Append(help_menu, "&Help")

        self.SetMenuBar(menu_bar)

        self.CreateStatusBar()
        self.SetStatusText("Welcome to wxPython!")

        icon = wx.Icon("images/logo.ico", type=wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        self.Bind(wx.EVT_MENU, self.on_hello, hello_item)
        self.Bind(wx.EVT_MENU, self.on_exit, exit_item)
        self.Bind(wx.EVT_MENU, self.on_about, about_item)
        self.Bind(wx.EVT_BUTTON, self.random_company, generate_button)
        self.Bind(wx.EVT_BUTTON, self.copy_to_clipboard, copy_to_clipboard_button)

        file_path = FilePath("_internal")

        read_csv_file = file_path.get("original_data/largest_companies_by_market_cap.csv")
        write_csv_file = file_path.get("data/largest_us_companies_by_market_cap.csv")

        check_write_file_path = Path(write_csv_file)
        if check_write_file_path.exists() == False:
            create_us_companies_csv(read_csv_file, write_csv_file)

        read_csv_file = file_path.get("data/largest_us_companies_by_market_cap.csv")

        self.companies = read_csv(read_csv_file)

    def on_exit(self, event):
        self.Close(True)

    def on_hello(self, event):
        wx.MessageBox("Hello again from wxPython")

    def on_about(self, event):
        wx.MessageBox("This is a wxPython Hello World sample", "About Hello World 2", wx.OK|wx.ICON_INFORMATION)

    def random_company(self, event):
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

        self.list_box.Clear()

        for i in range(len(indices)):
            index = indices[i]
            company_row = self.companies[index]
            company_name = html.unescape(company_row["Name"])
            self.list_box.Append(company_name)

    def copy_to_clipboard(self, event):
        index = self.list_box.GetSelection()
        if index != wx.NOT_FOUND:
            if wx.TheClipboard.Open():
                item_label = self.list_box.GetString(index)
                text = wx.TextDataObject(item_label)
                wx.TheClipboard.SetData(text)
                wx.TheClipboard.Close()

def main():
    app = wx.App()
    frame = WxApp(None, title="Random Company")
    frame.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()
