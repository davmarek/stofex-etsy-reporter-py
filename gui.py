import os
import tkinter as tk
from tkinter import filedialog

from reporter import load_and_report


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
        app_icon = tk.PhotoImage(file="icons/favicon.png")
        self.root.iconbitmap("icons/favicon.ico")
        self.root.iconphoto(False, app_icon)

        # Variables
        self.etsy_path = tk.StringVar()
        self.money_path = tk.StringVar()
        self.ls_path = tk.StringVar()
        self.save_dir_path = tk.StringVar()

        self.etsy_path.set(try_to_find_file("etsy.csv"))
        self.money_path.set(try_to_find_file("export.csv"))
        self.save_dir_path.set(os.getcwd())

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

        # ==== SAVE FOLDER ====
        # Create Save dir Frame
        frame_save_dir = tk.Frame(frame)
        frame_save_dir.grid(column=0, row=3, pady=5, sticky=tk.W)

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

    def select_save_dir_folder(self):
        path = select_folder("Select folder for reports")
        self.save_dir_path.set(path)

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
        self.root.geometry("+%d+%d" % (100, 100))
        # Start the GUI event loop
        self.root.mainloop()
