# Default filenames
DEFAULT_FILENAME_ETSY = "etsy.csv"
DEFAULT_FILENAME_MONEY = "export.csv"

# CSV column indexes
COLUMN_ETSY_SKU: int = 23
COLUMN_ETSY_TITLE: int = 0
COLUMN_MONEY_SKU: int = 3
COLUMN_MONEY_QUANTITY: int = 4
COLUMN_LS_SKU: int = 0
COLUMN_LS_QUANTITY: int = 1

# Filenames for different reports types
FILENAME_WRONG_SKU: str = "wrong_sku.csv"
FILENAME_LOW_STOCK: str = "low_stock.csv"
FILENAME_LOW_STOCK_SUB0: str = "low_stock_sub0.csv"
FILENAME_LOW_STOCK_SUB10: str = "low_stock_sub10.csv"
FILENAME_LOW_STOCK_SUB50: str = "low_stock_sub50.csv"
FILENAME_LOW_STOCK_NEW: str = "low_stock_new.csv"
FILENAME_RESTOCK: str = "restock.csv"

# Headers of CSV files
HEADER_WRONG_SKU = ("SKU", "Title")
HEADER_LOW_STOCK = ("SKU", "Quantity", "Etsy Title")
HEADER_RESTOCK = ("SKU", "Old Quantity", "New Quantity")
HEADER_LOW_STOCK_NEW = ("SKU", "Quantity")


# GUI Settings
GUI_WINDOW_PAD = 20
GUI_SECTION_PADY = 5