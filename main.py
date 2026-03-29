import random
import csv
import html
from pathlib import Path
import os
from PySide6 import QtCore, QtWidgets, QtGui
import sys

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

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, app: QtWidgets.QApplication):
        super().__init__()
        self.app = app
        # Set the application’s GUI style to dark mode
        self.app.setStyle("fusion")

        self.clipboard = self.app.clipboard()

        window_title = "Random Company"
        self.setWindowTitle(window_title)

        window_width = 300
        window_height = 350
        window_size = QtCore.QSize(window_width, window_height)
        self.setFixedSize(window_size)

        file_path = FilePath("_internal")
        logo_path = file_path.get("images/logo.ico")

        icon = QtGui.QIcon(logo_path)
        self.setWindowIcon(icon)

        self.text = QtWidgets.QLabel("Random Companies: ", alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        self.list_box = QtWidgets.QListView()
        list_box_height = 200
        self.list_box.setMinimumHeight(list_box_height)
        self.list_box.setMaximumHeight(list_box_height)
        self.model = QtGui.QStandardItemModel()
        self.list_box.setModel(self.model)

        self.generate_button = QtWidgets.QPushButton("Generate")
        button_width = 150
        button_height = 38
        button_size = QtCore.QSize(button_width, button_height)
        self.generate_button.setFixedSize(button_size)
        self.copy_to_clipboard_button = QtWidgets.QPushButton("Copy to Clipboard")
        self.copy_to_clipboard_button.setFixedSize(button_size)

        self.generate_button.clicked.connect(self.random_company)
        self.copy_to_clipboard_button.clicked.connect(self.copy_to_clipboard)

        central_widget = QtWidgets.QWidget()
        self.layout = QtWidgets.QVBoxLayout(central_widget)
        self.layout.addWidget(self.text, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.list_box, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.generate_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.copy_to_clipboard_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        self.setCentralWidget(central_widget)

        read_csv_file = file_path.get("original_data/largest_companies_by_market_cap.csv")
        write_csv_file = file_path.get("data/largest_us_companies_by_market_cap.csv")

        check_write_file_path = Path(write_csv_file)
        if check_write_file_path.exists() == False:
            create_us_companies_csv(read_csv_file, write_csv_file)

        read_csv_file = file_path.get("data/largest_us_companies_by_market_cap.csv")

        self.companies = read_csv(read_csv_file)

    @QtCore.Slot()
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

        self.model.clear()

        for i in range(len(indices)):
            index = indices[i]
            company_row = self.companies[index]
            company_name: str = html.unescape(company_row["Name"])
            item = QtGui.QStandardItem(company_name)
            self.model.appendRow(item)

    @QtCore.Slot()
    def copy_to_clipboard(self):
        indexes = self.list_box.selectedIndexes()

        if len(indexes) != 0:
            item_label = indexes[0]
            text = item_label.data()
            self.clipboard.setText(text)

def main():
    app = QtWidgets.QApplication([])

    window = MainWindow(app)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
