import os
import pandas as pd
from scripts import constants as c

EtsyData = dict[str, str]
MoneyData = dict[str, int]
LowStockData = dict[str, int]


def load_csv_data(filepath: str, sku_column: int, value_column: int, value_type: type):
    # Load the file if it exists
    df: pd.DataFrame
    if os.path.exists(filepath):
        # Load the file into a DataFrame
        delimiter = detect_delimiter(filepath)
        df = pd.read_csv(filepath, sep=delimiter, encoding="UTF8")
    else:
        print("The file does not exist:", filepath)
        exit(1)

    # Put the DataFrame into dict
    data = {}
    for _, row in df.iterrows():
        key: str = str(row[sku_column])

        # has commas inside SKU column = Etsy listing with variants
        if "," in key:
            # k = one SKU in one Etsy listing
            for k in key.split(","):
                val = str(row[value_column])
                # add SKU with title to returned data
                data[k] = val

        else:
            # MoneyData or LowStockData
            if value_type == int:
                val_string = str(row[value_column]).replace(",", ".")
                val_number = float(val_string)
                val = int(val_number)
            # EtsyData
            else:
                val = str(row[value_column])

            data[key] = val

    return data


def load_etsy_data(filepath: str) -> EtsyData:
    # value type is str = product title
    return load_csv_data(filepath, c.COLUMN_ETSY_SKU, c.COLUMN_ETSY_TITLE, value_type=str)


def load_money_data(filepath: str) -> MoneyData:
    # value type is int = quantity
    return load_csv_data(filepath, c.COLUMN_MONEY_SKU, c.COLUMN_MONEY_QUANTITY, value_type=int)


def load_ls_data(filepath: str) -> LowStockData:
    # value type is int = quantity
    return load_csv_data(filepath, c.COLUMN_LS_SKU, c.COLUMN_LS_QUANTITY, value_type=int)


def detect_delimiter(filepath):
    # Open the file in read-only mode
    with open(filepath, 'r', encoding="UTF8") as csvfile:
        # read the first row = header
        header = csvfile.readline()

        # count the number of commas and semicolons in the header row
        num_commas = header.count(',')
        num_semicolons = header.count(';')

        if num_semicolons > num_commas:
            return ';'
        else:
            return ','
