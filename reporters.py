from loaders import EtsyData, MoneyData, LowStockData


def report_wrong_sku(etsy: EtsyData, money: MoneyData) -> int:
    money_keys = money.keys()
    wrong = []

    for sku, title in etsy.items():
        if sku not in money_keys:
            wrong.append([sku, title])

    if len(wrong) > 0:
        print("Wrong SKUs found")
    else:
        print("No wrong SKUs found")

    return len(wrong)


def report_low_stock():
    pass


def report_new_low_stock():
    pass


def report_restock():
    pass
