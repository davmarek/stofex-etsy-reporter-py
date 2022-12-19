from tkinter import messagebox

from scripts.writer import write_data_to_cwd, write_data_to_report_folder
from scripts.loader import load_etsy_data, load_money_data, load_ls_data
from scripts.model import ProductList
import scripts.constants as c


class LowStockReport:
    def __init__(self, low_stock_data: ProductList, len_all: int, len_sub0: int, len_sub10: int, len_sub50: int):
        self.low_stock_data: ProductList = low_stock_data
        self.all: int = len_all
        self.sub0: int = len_sub0
        self.sub10: int = len_sub10
        self.sub50: int = len_sub50


def load_and_report(etsy_filepath: str, money_filepath: str, ols_filepath: str = ""):

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

    # ==== MESSAGE BOX ====

    message = \
        f"Wrong SKUs: {wrong_sku_count}\n" + \
        f"Low stock: {ls_report.all}\n"

    if restock_count > 0:
        message += f"\tRestock: {restock_count}\n"

    if new_low_stock_count > 0:
        message += f"\tNew low stock: {new_low_stock_count}\n"

    messagebox.showinfo("Result", message, icon="info")


def report_wrong_sku(etsy: ProductList, money: ProductList) -> int:
    # list of tuples [(SKU, title),...]
    wrong = [
        product.get_tuple(include_title=True)
        for sku, product in etsy.items()
        if sku not in money.keys()
    ]

    if len(wrong) > 0:
        print("Wrong SKUs found")
        write_data_to_report_folder(
            c.FILENAME_WRONG_SKU, wrong, c.HEADER_WRONG_SKU)
    else:
        print("No wrong SKUs found")

    return len(wrong)


def report_low_stock(etsy: ProductList, money: ProductList) -> LowStockReport:
    low_stock: ProductList = {
        money_sku: money_product
        for money_sku, money_product in money.items()
        if money_sku in etsy.keys() and money_product.quantity < 50
    }

    stock_sub0 = [
        (sku, product.quantity, etsy[sku].title)
        for sku, product in low_stock.items()
        if product.quantity <= 0
    ]

    stock_sub10 = [
        (sku, product.quantity, etsy[sku].title)
        for sku, product in low_stock.items()
        if 0 < product.quantity <= 10
    ]

    stock_sub50 = [
        (sku, product.quantity, etsy[sku].title)
        for sku, product in low_stock.items()
        if 10 < product.quantity <= 50
    ]

    stock_all = stock_sub0 + stock_sub10 + stock_sub50

    report = LowStockReport(
        low_stock_data=low_stock,
        len_all=len(stock_all),
        len_sub0=len(stock_sub0),
        len_sub10=len(stock_sub10),
        len_sub50=len(stock_sub50)
    )

    if report.all > 0:
        # write low stock report to cwd AND reports folder
        write_data_to_cwd(c.FILENAME_LOW_STOCK, stock_all, c.HEADER_LOW_STOCK)
        write_data_to_report_folder(
            c.FILENAME_LOW_STOCK, stock_all, c.HEADER_LOW_STOCK)

        # write all other files ONLY to reports folder
        if report.sub0 > 0:
            write_data_to_report_folder(
                c.FILENAME_LOW_STOCK_SUB0, stock_sub0, c.HEADER_LOW_STOCK)
        if report.sub10 > 0:
            write_data_to_report_folder(
                c.FILENAME_LOW_STOCK_SUB10, stock_sub10, c.HEADER_LOW_STOCK)
        if report.sub50 > 0:
            write_data_to_report_folder(
                c.FILENAME_LOW_STOCK_SUB50, stock_sub50, c.HEADER_LOW_STOCK)

    return report


def report_restock(ols: ProductList, money: ProductList) -> int:
    restock = [
        (money_sku, ols[money_sku].quantity, money_product.quantity)
        for money_sku, money_product in money.items()
        if
        money_sku in ols.keys()
        and money_product.quantity > 50
        and money_product.quantity > ols[money_sku].quantity
    ]

    restock_count = len(restock)
    if restock_count > 0:
        write_data_to_report_folder(
            c.FILENAME_RESTOCK, restock, c.HEADER_RESTOCK)

    return restock_count


def report_new_low_stock(ols: ProductList, ls: ProductList) -> int:
    nls = [
        ls_product.get_tuple()
        for ls_sku, ls_product in ls.items()
        if
        ls_sku not in ols.keys()
    ]

    nls_count = len(nls)
    if nls_count > 0:
        write_data_to_report_folder(
            c.FILENAME_LOW_STOCK_NEW, nls, c.HEADER_LOW_STOCK_NEW)

    return nls_count
