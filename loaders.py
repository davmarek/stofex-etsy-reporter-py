import os
import pandas as pd

EtsyData = dict[str, int]
MoneyData = dict[str, int]
LowStockData = dict[str, int]

EtsySKUColumn: int = 23
EtsyTitleColumn: int = 0
MoneySKUColumn: int = 3
MoneyQuantityColumn: int = 4
LsSKUColumn: int = 0
LsQuantityColumn: int = 1

FilenameLowStock: str = "low_stock.csv"
FilenameLowStockSub0: str = "low_stock_sub0.csv"
FilenameLowStockSub10: str = "low_stock_sub10.csv"
FilenameLowStockSub50: str = "low_stock_sub50.csv"
FilenameWrongSKU: str = "wrong_sku.csv"
FilenameRestock: str = "restocked.csv"
FilenameLowStockNew: str = "low_stock_new.csv"


def load_csv_data(filepath: str, sku_column: int, value_column: int, value_type: type):
    df: pd.DataFrame
    data = {}

    # Load the file if it exists
    if os.path.exists(filepath):
        # Load the file into a DataFrame
        df = pd.read_csv(filepath)
    else:
        print("The file does not exist:", filepath)
        exit(1)

    # Put the DataFrame into dict
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
    return load_csv_data(filepath, EtsySKUColumn, EtsyTitleColumn, value_type=str)


def load_money_data(filepath: str) -> MoneyData:
    return load_csv_data(filepath, MoneySKUColumn, MoneyQuantityColumn, value_type=int)


def load_ls_data(filepath: str) -> LowStockData:
    return load_csv_data(filepath, LsSKUColumn, LsQuantityColumn, value_type=int)
