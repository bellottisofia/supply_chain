# simulation.py

from supply_chain import SupplyChainManager
import random
from utils import TimeSimulator

def run_simulation():
    scm = SupplyChainManager()
    time_simulator = TimeSimulator()

    # Define entities
    suppliers = ['SupplierA', 'SupplierB']
    manufacturers = ['ManufacturerA', 'ManufacturerB']
    logistics_providers = ['LogisticsA', 'LogisticsB']
    retailers = ['RetailerA', 'RetailerB']
    consumers = ['ConsumerA', 'ConsumerB']

    # Assign roles to entities
    for supplier in suppliers:
        scm.assign_role('supplier', supplier)
    for manufacturer in manufacturers:
        scm.assign_role('manufacturer', manufacturer)
    for logistics in logistics_providers:
        scm.assign_role('logistics', logistics)
    for retailer in retailers:
        scm.assign_role('retailer', retailer)
    for consumer in consumers:
        scm.assign_role('consumer', consumer)

    # Define possible origins
    origins = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']

    # Number of products to simulate
    num_products = 10

    # Create multiple products
    product_ids = [f"PROD{str(i).zfill(3)}" for i in range(1, num_products + 1)]

    for product_id in product_ids:
        # Randomly select a supplier and origin
        supplier = random.choice(suppliers)
        origin = random.choice(origins)

        # Supplier creates a product
        try:
            current_time = time_simulator.get_time_str()
            product = scm.create_product(product_id, origin, supplier, date=current_time)
            print(f"Product created: {product.product_id} at {product.origin} by {supplier} at {current_time}")
        except Exception as e:
            print(f"Error creating product {product_id}: {e}")
            continue

        # Advance time after creation
        time_simulator.advance_time(min_hours=1, max_hours=12)

        # Manufacturer updates product status to 'Manufactured'
        manufacturer = random.choice(manufacturers)
        try:
            current_time = time_simulator.get_time_str()
            scm.update_product_status(product_id, 'Manufactured', manufacturer, date=current_time)
            print(f"Product {product_id} status updated to 'Manufactured' by {manufacturer} at {current_time}")
        except Exception as e:
            print(f"Error updating product {product_id} to 'Manufactured': {e}")
            continue

        # Advance time after manufacturing
        time_simulator.advance_time(min_hours=12, max_hours=48)

        # Logistics updates product status to 'In Transit'
        logistics = random.choice(logistics_providers)
        try:
            current_time = time_simulator.get_time_str()
            scm.update_product_status(product_id, 'In Transit', logistics, date=current_time)
            print(f"Product {product_id} status updated to 'In Transit' by {logistics} at {current_time}")
        except Exception as e:
            print(f"Error updating product {product_id} to 'In Transit': {e}")
            continue

        # Advance time during transit
        time_simulator.advance_time(min_hours=24, max_hours=72)

        # Retailer updates product status to 'Available for Sale'
        retailer = random.choice(retailers)
        try:
            current_time = time_simulator.get_time_str()
            scm.update_product_status(product_id, 'Available for Sale', retailer, date=current_time)
            print(f"Product {product_id} status updated to 'Available for Sale' by {retailer} at {current_time}")
        except Exception as e:
            print(f"Error updating product {product_id} to 'Available for Sale': {e}")
            continue

        # Advance time before purchase
        time_simulator.advance_time(min_hours=1, max_hours=72)

        # Consumer purchases the product
        consumer = random.choice(consumers)
        try:
            current_time = time_simulator.get_time_str()
            scm.update_product_status(product_id, 'Purchased', consumer, date=current_time)
            print(f"Product {product_id} status updated to 'Purchased' by {consumer} at {current_time}")
        except Exception as e:
            print(f"Error updating product {product_id} to 'Purchased': {e}")
            continue

        # Advance time before the next product
        time_simulator.advance_time(min_hours=6, max_hours=24)

    # Mine pending transactions into blocks
    while scm.blockchain.mempool:
        new_block = scm.blockchain.new_block()
        new_block.mine()
        scm.blockchain.extend_chain(new_block)
        print(f"New block mined and added to the blockchain. Block index: {new_block.index}")

    return scm

if __name__ == "__main__":
    scm = run_simulation()