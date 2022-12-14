from dataclasses import dataclass


@dataclass
class Product:
    sku: int
    quantity: int = None
    title: str = None

    def get_tuple(self, include_quantity: bool = True, include_title: bool = False) -> tuple:
        tuple_ = (self.sku,)

        if include_quantity and self.quantity is not None:
            tuple_ += (self.quantity,)

        if include_title and self.title is not None:
            tuple_ += (self.title,)

        return tuple_


ProductList = dict[str, Product]
