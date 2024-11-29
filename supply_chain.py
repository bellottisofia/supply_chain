# supply_chain.py

from roles import Roles
from product import Product
from transaction import Transaction
from blockchain import Blockchain
from ecdsa import SigningKey

class SupplyChainManager:
    def __init__(self):
        self.roles = Roles()
        self.products = {}
        self.blockchain = Blockchain()
        self.entity_keys = {}  # Store private keys for entities

    def assign_role(self, role, entity):
        self.roles.assign_role(role, entity)
        # Generate a private key for the entity
        sk = SigningKey.generate()
        self.entity_keys[entity] = sk

    def get_entity_private_key(self, entity):
        return self.entity_keys.get(entity)

    def create_product(self, product_id, origin, creator, date=None):
        if not self.roles.has_role('supplier', creator):
            raise PermissionError("Creator does not have supplier role")
        if product_id in self.products:
            raise ValueError("Product already exists")
        product = Product(product_id, origin, creator, date=date)
        self.products[product_id] = product
        # Create a transaction for product creation
        transaction = Transaction(
            product_id=product_id,
            event="ProductCreated",
            date=date  # Pass the date here
        )
        # Sign the transaction with creator's private key
        creator_private_key = self.get_entity_private_key(creator)
        transaction.sign(creator_private_key)
        self.blockchain.add_transaction(transaction)
        return product

    def update_product_status(self, product_id, status, updater, date=None):
        product = self.products.get(product_id)
        if not product:
            raise ValueError("Product does not exist")
        # Check if updater has the correct role for the status
        role_required = self.get_role_for_status(status)
        if not role_required:
            raise ValueError(f"No role associated with status '{status}'")
        if not self.roles.has_role(role_required, updater):
            raise PermissionError(f"Updater does not have {role_required} role")
        product.update_status(status, updater, date=date)
        # Create a transaction for status update
        transaction = Transaction(
            product_id=product_id,
            event=f"StatusUpdated to {status}",
            date=date  # Pass the date here
        )
        # Sign the transaction with updater's private key
        updater_private_key = self.get_entity_private_key(updater)
        transaction.sign(updater_private_key)
        self.blockchain.add_transaction(transaction)

    def get_product_details(self, product_id):
        product = self.products.get(product_id)
        if not product:
            raise ValueError("Product does not exist")
        return product

    def get_product_history(self, product_id):
        product = self.get_product_details(product_id)
        return product.get_history()

    def get_role_for_status(self, status):
        status_role_map = {
            "Manufactured": "manufacturer",
            "In Transit": "logistics",
            "Available for Sale": "retailer",
            "Purchased": "consumer",
            # Add more statuses as needed
        }
        return status_role_map.get(status, None)