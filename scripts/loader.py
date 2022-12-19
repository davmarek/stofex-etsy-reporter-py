import os
from csv import Sniffer

import pandas as pd

import scripts.constants as c
from scripts.model import ProductList, Product


def load_csv_data(filepath: str,
                  sku_column: int,
                  quantity_column: int | None = None,
                  title_column: int | None = None
                  ) -> ProductList:
    # Load the file if it exists
    df: pd.DataFrame
    if os.path.exists(filepath):
        # Load the file into a DataFrame
        delimiter = detect_delimiter(filepath)
        df = pd.read_csv(filepath, sep=delimiter, encoding="UTF8")
    else:
        print("The file does not exist:", filepath)
        raise FileNotFoundError

    # Put the DataFrame into dict of Products
    data = {}
    for _, row in df.iterrows():
        sku: str = str(row[sku_column])

        # Money or Low Stock
        if quantity_column is not None:
            quantity_string = str(row[quantity_column]).replace(",", ".")
            quantity = int(float(quantity_string))
            data[sku] = Product(sku, quantity=quantity)

        # Etsy
        elif title_column is not None:
            # has commas inside SKU column = Etsy listing with variants
            if "," in sku:
                # sku_variant = one SKU in one Etsy listing
                for sku_variant in sku.split(","):
                    data[sku_variant] = Product(sku_variant, title=row[title_column])

            else:
                data[sku] = Product(sku, title=row[title_column])

    return data


def load_etsy_data(filepath: str) -> ProductList:
    # value type is str = product title
    return load_csv_data(filepath, sku_column=c.COLUMN_ETSY_SKU, title_column=c.COLUMN_ETSY_TITLE)


def load_money_data(filepath: str) -> ProductList:
    # value type is int = quantity
    return load_csv_data(filepath, sku_column=c.COLUMN_MONEY_SKU, quantity_column=c.COLUMN_MONEY_QUANTITY)


def load_ls_data(filepath: str) -> ProductList:
    # value type is int = quantity
    return load_csv_data(filepath, sku_column=c.COLUMN_LS_SKU, quantity_column=c.COLUMN_LS_QUANTITY)


def detect_delimiter(filepath):
    with open(filepath, 'r', encoding="UTF8") as csvfile:
        # Use the csv module's Sniffer class to automatically detect the delimiter
        dialect = Sniffer().sniff(csvfile.read(1024))
        return dialect.delimiter
