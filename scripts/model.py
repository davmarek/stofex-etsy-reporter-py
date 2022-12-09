class Product:
    def __init__(self, sku: int, quantity: int = None, title: str = None):
        self.sku = sku
        self.quantity = quantity
        self.title = title

    def get_tuple(self, include_quantity: bool = True, include_title: bool = False) -> tuple:
        tuple_ = (self.sku,)

        if include_quantity and self.quantity is not None:
            tuple_ += (self.quantity,)

        if include_title and self.title is not None:
            tuple_ += (self.title,)

        return tuple_


ProductList = dict[str, Product]
