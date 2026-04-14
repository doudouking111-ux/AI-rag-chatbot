from langchain_core.tools import tool

# Simulated database
INVENTORY = {
    "Americano": 50, "Latte": 30, "Cappuccino": 20,
    "Mocha": 15, "Matcha Latte": 10, "Iced Lemon Tea": 40,
}
ORDERS = []
RESERVATIONS = []


@tool
def check_inventory(drink_name: str) -> str:
    """Check the inventory quantity of a drink."""
    qty = INVENTORY.get(drink_name)
    if qty is None:
        return f"Drink '{drink_name}' not found."
    return f"'{drink_name}' has {qty} cups in stock."


@tool
def create_order(drink_name: str, quantity: int) -> str:
    """Create a drink order. drink_name is the drink name, quantity is 1-10."""
    if quantity < 1 or quantity > 10:
        return "Order quantity must be between 1 and 10."
    stock = INVENTORY.get(drink_name, 0)
    if stock < quantity:
        return f"Insufficient stock: '{drink_name}' only has {stock} cups left."
    INVENTORY[drink_name] -= quantity
    order_id = len(ORDERS) + 1
    ORDERS.append({"id": order_id, "drink": drink_name, "qty": quantity})
    return f"Order created! Order #{order_id}: {drink_name} x{quantity}."


@tool
def reserve_seat(date: str, time: str, num_people: int) -> str:
    """Reserve a seat. date format YYYY-MM-DD, time format HH:MM, num_people is party size."""
    res_id = len(RESERVATIONS) + 1
    RESERVATIONS.append({"id": res_id, "date": date, "time": time, "people": num_people})
    return f"Reservation confirmed! #{res_id}: {date} {time}, {num_people} people."
