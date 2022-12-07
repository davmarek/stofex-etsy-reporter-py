from writer import write_data_to_cwd, write_data_to_report_folder
from loader import load_etsy_data, load_money_data, load_ls_data, EtsyData, MoneyData, LowStockData
from tkinter import messagebox

import constants as c


class LowStockStats():
    def __init__(self, len_all: int, len_sub0: int, len_sub10: int, len_sub50: int):
        self.all: int = len_all
        self.sub0: int = len_sub0
        self.sub10: int = len_sub10
        self.sub50: int = len_sub50


def load_and_report(etsy_filepath: str, money_filepath: str, ls_filepath: str = ""):
    # ==== FILE LOADING ====
    etsy = load_etsy_data(etsy_filepath)
    money = load_money_data(money_filepath)

    print("Etsy SKUs:", len(etsy))
    print("Money SKUs:", len(money))

    if ls_filepath != "":
        ls = load_ls_data(ls_filepath)
        print("Low Stock SKUs:", len(ls))

    # ==== REPORTING ====
    wrong_len = report_wrong_sku(etsy, money)
    ls_stats = report_low_stock(etsy, money)

    # ==== MESSAGE BOX ====

    message = \
        f"Wrong SKUs: {wrong_len}\n" + \
        f"Low stock: {ls_stats.all}\n"

    if ls_stats.all > 0:
        message += \
            f"\tSub0: {ls_stats.sub0}\n" + \
            f"\tSub10: {ls_stats.sub10}\n" + \
            f"\tSub50: {ls_stats.sub50}\n"

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


def report_low_stock(etsy: EtsyData, money: MoneyData) -> LowStockStats:
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
            # this will become one row in the CSV file
            row = (etsy_sku, money_quantity, etsy[etsy_sku])

            stock_all.append(row)

            if money_quantity <= 0:
                stock_sub0.append(row)
            elif money_quantity <= 10:
                stock_sub10.append(row)
            else:
                stock_sub50.append(row)

    stats = LowStockStats(
        len_all=len(stock_all),
        len_sub0=len(stock_sub0),
        len_sub10=len(stock_sub10),
        len_sub50=len(stock_sub50)
    )

    if stats.all > 0:
        # write low stock report to cwd AND reports folder
        write_data_to_cwd(c.FILENAME_LOW_STOCK, stock_all, c.HEADER_LOW_STOCK)
        write_data_to_report_folder(c.FILENAME_LOW_STOCK, stock_all, c.HEADER_LOW_STOCK)

        # write all other files ONLY to reports folder
        if stats.sub0 > 0:
            write_data_to_report_folder(c.FILENAME_LOW_STOCK_SUB0, stock_sub0, c.HEADER_LOW_STOCK)
        if stats.sub10 > 0:
            write_data_to_report_folder(c.FILENAME_LOW_STOCK_SUB10, stock_sub10, c.HEADER_LOW_STOCK)
        if stats.sub50 > 0:
            write_data_to_report_folder(c.FILENAME_LOW_STOCK_SUB50, stock_sub50, c.HEADER_LOW_STOCK)

    return stats


def report_new_low_stock():
    pass


def report_restock():
    pass
