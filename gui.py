import os
import tkinter as tk
from tkinter import filedialog

from loaders import load_etsy_data, load_money_data, load_ls_data
from reporters import report_wrong_sku


def load_and_report(etsy_filepath: str, money_filepath: str, ls_filepath: str = ""):
    etsy = load_etsy_data(etsy_filepath)
    money = load_money_data(money_filepath)

    print("Etsy SKUs:", len(etsy))
    print("Money SKUs:", len(money))

    if ls_filepath != "":
        ls = load_ls_data(ls_filepath)
        print("Low Stock SKUs:", len(ls))

    report_wrong_sku(etsy, money)


def set_entry_value(entry: tk.Entry, value: str):
    entry.configure(state=tk.NORMAL)
    end = entry.index(tk.END)
    entry.delete(0, end)
    entry.insert(0, value)
    entry.configure(state=tk.DISABLED)


def select_csv_file(title: str) -> str:
    filename = filedialog.askopenfilename(title=title, filetypes=[("CSV files", "csv")])
    if filename == "":
        print("No filename selected")
        return ""

    if not os.path.exists(filename):
        print(filename, "doesn't exist")
        return ""

    return filename


def select_folder(title: str) -> str:
    path = filedialog.askdirectory(title=title, initialdir=os.getcwd())
    if path == "":
        print("No folder selected")
        return ""

    if not os.path.exists(path):
        print(path, "doesn't exist")
        return ""

    return path


def try_to_find_file(filename: str) -> str:
    if os.path.exists(filename):
        real_path = os.path.realpath(filename)
        return real_path
    else:
        return ""


class Window:
    def __init__(self):
        # Create the main window
        self.root = tk.Tk()
        self.root.title("Etsy Reporter")

        # Variables
        self.etsy_path = tk.StringVar()
        self.money_path = tk.StringVar()
        self.ls_path = tk.StringVar()
        self.report_path = tk.StringVar()

        self.etsy_path.set(try_to_find_file("etsy.csv"))
        self.money_path.set(try_to_find_file("export.csv"))
        self.report_path.set(os.getcwd())

        # Main wrapping frame
        frame = tk.Frame(self.root)
        frame.pack(padx=20, pady=20)

        # ==== ETSY ====
        # Create Etsy Frame
        frame_etsy = tk.Frame(frame)
        frame_etsy.grid(column=0, row=0, pady=5, sticky=tk.W)

        # Etsy label
        tk.Label(frame_etsy, text="Etsy CSV").grid(column=0, row=0, sticky=tk.W)

        # Etsy filepath input
        self.etsy_input = tk.Entry(frame_etsy, textvariable=self.etsy_path, state=tk.DISABLED, width=60)
        self.etsy_input.grid(column=0, row=1)

        # Etsy browse button
        etsy_button_browse = tk.Button(frame_etsy, text="Select file", command=self.select_etsy)
        etsy_button_browse.grid(column=1, row=1)

        # ==== MONEY ====
        # Create Money Frame
        frame_money = tk.Frame(frame)
        frame_money.grid(column=0, row=1, pady=5, sticky=tk.W)

        # Money label
        tk.Label(frame_money, text="Money CSV").grid(column=0, row=0, sticky=tk.W)

        # Money filepath input
        self.money_input = tk.Entry(frame_money, textvariable=self.money_path, state=tk.DISABLED, width=60)
        self.money_input.grid(column=0, row=1)

        # Money browse button
        money_button_browse = tk.Button(frame_money, text="Select file", command=self.select_money)
        money_button_browse.grid(column=1, row=1)

        # ==== LOW STOCK ====
        # Create Low stock Frame
        frame_ls = tk.Frame(frame)
        frame_ls.grid(column=0, row=2, pady=5, sticky=tk.W)

        # Low stock label
        tk.Label(frame_ls, text="Low stock CSV").grid(column=0, row=0, sticky=tk.W)

        # Low stock filepath input
        self.ls_input = tk.Entry(frame_ls, textvariable=self.ls_path, state=tk.DISABLED, width=60)
        self.ls_input.grid(column=0, row=1)

        # Low stock browse button
        ls_button_browse = tk.Button(frame_ls, text="Select file", command=self.select_low_stock)
        ls_button_browse.grid(column=1, row=1)

        # ==== REPORT FOLDER ====
        # Create Low stock Frame
        frame_report = tk.Frame(frame)
        frame_report.grid(column=0, row=3, pady=5, sticky=tk.W)

        # Low stock label
        tk.Label(frame_report, text="Report Folder").grid(column=0, row=0, sticky=tk.W)

        # Low stock filepath input
        self.report_input = tk.Entry(frame_report, textvariable=self.report_path, state=tk.DISABLED, width=60)
        self.report_input.grid(column=0, row=1)

        # Low stock browse button
        report_button_browse = tk.Button(frame_report, text="Select folder", command=self.select_report_folder)
        report_button_browse.grid(column=1, row=1)

        # ==== GENERATE REPORT ====
        # Report button
        report_button = tk.Button(frame, text="Generate Report", command=self.generate_report)
        report_button.grid(column=0, row=4, pady=5, ipady=5, sticky="news")

    def select_etsy(self):
        filepath = select_csv_file("Select Etsy CSV")
        self.etsy_path.set(filepath)

    def select_money(self):
        filepath = select_csv_file("Select Money CSV")
        self.money_path.set(filepath)

    def select_low_stock(self):
        filepath = select_csv_file("Select Low stock CSV")
        self.ls_path.set(filepath)

    def select_report_folder(self):
        path = select_folder("Select folder for reports")
        self.report_path.set(path)

    def generate_report(self):
        etsy_filepath = self.etsy_path.get()
        money_filepath = self.money_path.get()
        ls_filepath = self.ls_path.get()

        if etsy_filepath == "":
            print("Etsy filepath empty")

        if money_filepath == "":
            print("Money filepath empty")

        load_and_report(etsy_filepath, money_filepath, ls_filepath)

    def start(self):
        # Start the GUI event loop
        self.root.mainloop()
