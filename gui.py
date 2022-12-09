import os
import tkinter as tk
from tkinter import filedialog

from scripts.reporter import load_and_report
from scripts import constants as c


# FAVICON_ICO = "./icons/favicon.ico"
# FAVICON_PNG = "./icons/favicon.png"


def set_entry_value(entry: tk.Entry, value: str):
    entry.configure(state=tk.NORMAL)
    end = entry.index(tk.END)
    entry.delete(0, end)
    entry.insert(0, value)
    entry.configure(state=tk.DISABLED)


def select_csv_file(title: str) -> str:
    filename = filedialog.askopenfilename(title=title, filetypes=[("CSV files", "csv")], initialdir=os.getcwd())
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

        # Main windows settings
        self.root.title("Etsy Reporter")

        # Variables
        self.etsy_path = tk.StringVar()
        self.money_path = tk.StringVar()
        self.ls_path = tk.StringVar()
        self.save_dir_path = tk.StringVar()

        self.etsy_path.set(try_to_find_file(c.DEFAULT_FILENAME_ETSY))
        self.money_path.set(try_to_find_file(c.DEFAULT_FILENAME_MONEY))
        self.save_dir_path.set(os.getcwd())

        # Errors Strings
        self.etsy_error = tk.StringVar()
        self.money_error = tk.StringVar()

        # Main wrapping frame
        frame = tk.Frame(self.root)
        frame.pack(padx=c.GUI_WINDOW_PAD, pady=c.GUI_WINDOW_PAD)

        # ==== ETSY ====
        # Create Etsy Frame
        frame_etsy = tk.Frame(frame)
        frame_etsy.grid(column=0, row=0, sticky=tk.W)

        # Etsy label
        tk.Label(frame_etsy, text="Etsy CSV").grid(column=0, row=0, sticky=tk.W)

        # Etsy filepath input
        self.etsy_input = tk.Entry(frame_etsy, textvariable=self.etsy_path, state=tk.DISABLED, width=60)
        self.etsy_input.grid(column=0, row=1)

        # Etsy browse button
        etsy_button_browse = tk.Button(frame_etsy, text="Select file", command=self.select_etsy)
        etsy_button_browse.grid(column=1, row=1)

        # Etsy error
        etsy_error_label = tk.Label(frame_etsy, textvariable=self.etsy_error, fg="red")
        etsy_error_label.grid(column=0, row=2, columnspan=2, sticky=tk.W)

        # ==== MONEY ====
        # Create Money Frame
        frame_money = tk.Frame(frame)
        frame_money.grid(column=0, row=1, sticky=tk.W)

        # Money label
        tk.Label(frame_money, text="Money CSV").grid(column=0, row=0, sticky=tk.W)

        # Money filepath input
        self.money_input = tk.Entry(frame_money, textvariable=self.money_path, state=tk.DISABLED, width=60)
        self.money_input.grid(column=0, row=1)

        # Money browse button
        money_button_browse = tk.Button(frame_money, text="Select file", command=self.select_money)
        money_button_browse.grid(column=1, row=1)

        # Money error
        money_error_label = tk.Label(frame_money, textvariable=self.money_error, fg="red")
        money_error_label.grid(column=0, row=2, columnspan=2, sticky=tk.W)

        # ==== LOW STOCK ====
        # Create Low stock Frame
        frame_ls = tk.Frame(frame)
        frame_ls.grid(column=0, row=2, pady=c.GUI_SECTION_PADY, sticky=tk.W)

        # Low stock label
        tk.Label(frame_ls, text="Low stock CSV").grid(column=0, row=0, sticky=tk.W)

        # Low stock filepath input
        self.ls_input = tk.Entry(frame_ls, textvariable=self.ls_path, state=tk.DISABLED, width=60)
        self.ls_input.grid(column=0, row=1)

        # Low stock browse button
        ls_button_browse = tk.Button(frame_ls, text="Select file", command=self.select_low_stock)
        ls_button_browse.grid(column=1, row=1)

        # ==== SAVE FOLDER ====
        # Create Save dir Frame
        frame_save_dir = tk.Frame(frame)
        frame_save_dir.grid(column=0, row=3, pady=c.GUI_SECTION_PADY, sticky=tk.W)

        # Save dir label
        tk.Label(frame_save_dir, text="Save Folder").grid(column=0, row=0, sticky=tk.W)

        # Save dir filepath input
        self.save_dir_input = tk.Entry(frame_save_dir, textvariable=self.save_dir_path, state="readonly", width=60)
        self.save_dir_input.grid(column=0, row=1, columnspan=2)

        # Low stock browse button
        # save_dir_button_browse = tk.Button(frame_save_dir, text="Select folder", command=self.select_save_dir_folder)
        # save_dir_button_browse.grid(column=1, row=1)

        # ==== GENERATE REPORT ====
        # Report button
        report_button = tk.Button(frame, text="Generate Report", command=self.generate_report)
        report_button.grid(column=0, row=4, pady=(c.GUI_SECTION_PADY, 0), ipady=5, sticky="news")

    def select_etsy(self):
        filepath = select_csv_file("Select Etsy CSV")
        if filepath != "":
            self.etsy_path.set(filepath)
            self.etsy_error.set("")

    def select_money(self):
        filepath = select_csv_file("Select Money CSV")
        if filepath != "":
            self.money_path.set(filepath)
            self.money_error.set("")

    def select_low_stock(self):
        filepath = select_csv_file("Select Low stock CSV")
        self.ls_path.set(filepath)

    def select_save_dir_folder(self):
        path = select_folder("Select folder for reports")
        self.save_dir_path.set(path)

    def generate_report(self):
        etsy_filepath = self.etsy_path.get()
        money_filepath = self.money_path.get()
        ls_filepath = self.ls_path.get()

        self.etsy_error.set("")
        if etsy_filepath == "":
            print("Etsy filepath empty")
            self.etsy_error.set("Etsy filepath empty")
            return

        self.money_error.set("")
        if money_filepath == "":
            print("Money filepath empty")
            self.money_error.set("Money filepath empty")
            return

        load_and_report(etsy_filepath, money_filepath, ls_filepath)

    def start(self):
        self.root.geometry("+%d+%d" % (100, 100))
        # Start the GUI event loop
        self.root.mainloop()
