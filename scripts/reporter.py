from tkinter import messagebox
from time import time
import threading

from scripts.writer import write_data_to_cwd, write_data_to_report_folder
from scripts.loader import load_etsy_data, load_money_data, load_ls_data, EtsyData, MoneyData, LowStockData
from scripts import constants as c


class LowStockReport:
    def __init__(self, low_stock_data: LowStockData, len_all: int, len_sub0: int, len_sub10: int, len_sub50: int):
        self.low_stock_data: LowStockData = low_stock_data
        self.all: int = len_all
        self.sub0: int = len_sub0
        self.sub10: int = len_sub10
        self.sub50: int = len_sub50


def load_and_report(etsy_filepath: str, money_filepath: str, ols_filepath: str = ""):
    time_start = time()

    # ==== FILE LOADING ====
    # load both mandatory files
    etsy_data = load_etsy_data(etsy_filepath)
    money_data = load_money_data(money_filepath)

    print("Etsy SKUs:", len(etsy_data))
    print("Money SKUs:", len(money_data))

    # ==== REPORTING ====

    # wrong SKUs
    wrong_sku_count = report_wrong_sku(etsy_data, money_data)

    # current low stock data from current Etsy and Money data
    ls_report = report_low_stock(etsy_data, money_data)
    ls_data = ls_report.low_stock_data

    # ==== OLD LOW STOCK ====
    restock_count = 0
    new_low_stock_count = 0

    # if user set the path to old low stock file, load it
    if ols_filepath != "":
        ols_data = load_ls_data(ols_filepath)
        print("Low Stock SKUs:", len(ols_data))

        restock_count = report_restock(ols_data, money_data)
        new_low_stock_count = report_new_low_stock(ols_data, ls_data)

    # ==== REPORT TIME ====

    time_end = time()

    time_result = time_end - time_start
    print("Time:", time_result)

    # ==== MESSAGE BOX ====

    message = \
        f"Wrong SKUs: {wrong_sku_count}\n" + \
        f"Low stock: {ls_report.all}\n"

    if restock_count > 0:
        message += f"\tRestock: {restock_count}\n"

    if new_low_stock_count > 0:
        message += f"\tNew low stock: {new_low_stock_count}\n"

    messagebox.showinfo("Result", message, icon="info")


def report_wrong_sku(etsy: EtsyData, money: MoneyData) -> int:
    money_keys = money.keys()
    wrong: list[tuple] = []  # list of tuples [(SKU, title),...]

    for sku, title in etsy.items():
        if sku not in money_keys:
            wrong.append((sku, title))

    if len(wrong) > 0:
        print("Wrong SKUs found")
        write_data_to_report_folder(c.FILENAME_WRONG_SKU, wrong, c.HEADER_WRONG_SKU)
    else:
        print("No wrong SKUs found")

    return len(wrong)


def report_low_stock(etsy: EtsyData, money: MoneyData) -> LowStockReport:
    # dict with all data
    low_stock: LowStockData = {}

    # lists with data for csv files
    stock_sub0 = []
    stock_sub10 = []
    stock_sub50 = []
    stock_all = []

    for etsy_sku in etsy.keys():
        money_quantity: int

        # check if Etsy SKU is in Money
        try:
            money_quantity = money[etsy_sku]
        except KeyError:
            # Etsy SKU isn't in Money
            continue

        if money_quantity < 50:
            low_stock[etsy_sku] = money_quantity

            # this will become one row in the CSV file
            row = (etsy_sku, money_quantity, etsy[etsy_sku])

            stock_all.append(row)

            if money_quantity <= 0:
                stock_sub0.append(row)
            elif money_quantity <= 10:
                stock_sub10.append(row)
            else:
                stock_sub50.append(row)

    report :LowStockReport= LowStockReport(
        low_stock_data=low_stock,
        len_all=len(stock_all),
        len_sub0=len(stock_sub0),
        len_sub10=len(stock_sub10),
        len_sub50=len(stock_sub50)
    )

    if report.all > 0:
        print("writing low stock")
        # write low stock report to cwd AND reports folder
        write_data_to_cwd(c.FILENAME_LOW_STOCK, stock_all, c.HEADER_LOW_STOCK)
        write_data_to_report_folder(c.FILENAME_LOW_STOCK, stock_all, c.HEADER_LOW_STOCK)

        # write all other files ONLY to reports folder
        if report.sub0 > 0:
            write_data_to_report_folder(c.FILENAME_LOW_STOCK_SUB0, stock_sub0, c.HEADER_LOW_STOCK)
        if report.sub10 > 0:
            write_data_to_report_folder(c.FILENAME_LOW_STOCK_SUB10, stock_sub10, c.HEADER_LOW_STOCK)
        if report.sub50 > 0:
            write_data_to_report_folder(c.FILENAME_LOW_STOCK_SUB50, stock_sub50, c.HEADER_LOW_STOCK)

    return report


def report_restock(ols_data: LowStockData, money_data: MoneyData) -> int:
    restock = []
    for ols_sku in ols_data.keys():
        try:
            new_quantity = money_data[ols_sku]
        except KeyError:
            continue

        old_quantity = ols_data[ols_sku]
        if (new_quantity > old_quantity) and (new_quantity >= 50):
            restock.append((ols_sku, old_quantity, new_quantity))

    restock_count = len(restock)
    if restock_count > 0:
        write_data_to_report_folder(c.FILENAME_RESTOCK, restock, c.HEADER_RESTOCK)

    return restock_count


def report_new_low_stock(ols_data: LowStockData, ls_data: LowStockData) -> int:
    low_stock_new = []
    for ls_sku in ls_data.keys():
        try:
            _ = ols_data[ls_sku]
            # continue if NEW low_stock is in OLD low_stock
            continue
        except KeyError:
            # ignore error
            low_stock_new.append((ls_sku, ls_data[ls_sku]))

    new_low_stock_count = len(low_stock_new)
    if new_low_stock_count > 0:
        write_data_to_report_folder(c.FILENAME_LOW_STOCK_NEW, low_stock_new, c.HEADER_LOW_STOCK_NEW)

    return new_low_stock_count
