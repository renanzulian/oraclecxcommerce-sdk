from oraclecxcommerce.services import OccSession


class ProductsModule:
    def __init__(self, occ_session: OccSession):
        self.session = occ_session
