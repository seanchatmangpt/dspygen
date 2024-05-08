import logging


# Setup basic configuration for logging
logging.basicConfig(level=logging.INFO, format='== APP == %(asctime)s %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# Business logic functions
def notify_activity(message):
    """Log notifications about the workflow."""
    logging.info(message)


def process_payment_activity(order_id, amount):
    """Process and authorize the payment for an order."""
    # REST API call to payment gateway
    # mock_stripe_api(order_id, amount)
    logging.info(f"Processing payment: {order_id} for ${amount}")
    return True


def verify_inventory_activity(item_name, quantity, inventory):
    """Check if there is enough inventory present for the purchase."""
    available = inventory.get(item_name, 0)
    if available >= quantity:
        logging.info(f"VerifyInventoryActivity: There are {available} {item_name}s available for purchase")
        return True
    else:
        logging.info("VerifyInventoryActivity: Insufficient inventory!")
        return False


def update_inventory_activity(item_name, quantity, inventory):
    """Remove the requested items from inventory and update the store."""
    if inventory[item_name] >= quantity:
        inventory[item_name] -= quantity
        logging.info(f"UpdateInventoryActivity: There are now {inventory[item_name]} {item_name}s left in stock")
        return True
    else:
        logging.error(f"UpdateInventoryActivity: Failed to update inventory for {item_name}")
        return False


def request_approval_activity(order_id, amount):
    """Request manager's approval if the payment amount is over $50,000."""
    if amount > 50000:
        logging.info(f"RequestApprovalActivity: Requesting approval for payment of ${amount} USD for order {order_id}")
        return True
    return False