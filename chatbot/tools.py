from langchain_core.tools import tool

# 模拟数据库
INVENTORY = {
    "美式咖啡": 50, "拿铁": 30, "卡布奇诺": 20,
    "摩卡": 15, "抹茶拿铁": 10, "冰柠檬茶": 40,
}
ORDERS = []
RESERVATIONS = []


@tool
def check_inventory(drink_name: str) -> str:
    """查询某个饮品的库存数量。"""
    qty = INVENTORY.get(drink_name)
    if qty is None:
        return f"没有找到「{drink_name}」这个饮品。"
    return f"「{drink_name}」当前库存 {qty} 杯。"


@tool
def create_order(drink_name: str, quantity: int) -> str:
    """创建一个饮品订单。drink_name 是饮品名称，quantity 是数量（1-10）。"""
    if quantity < 1 or quantity > 10:
        return "每笔订单数量需在 1-10 杯之间。"
    stock = INVENTORY.get(drink_name, 0)
    if stock < quantity:
        return f"库存不足，「{drink_name}」仅剩 {stock} 杯。"
    INVENTORY[drink_name] -= quantity
    order_id = len(ORDERS) + 1
    ORDERS.append({"id": order_id, "drink": drink_name, "qty": quantity})
    return f"订单创建成功！订单号：{order_id}，{drink_name} x{quantity}。"


@tool
def reserve_seat(date: str, time: str, num_people: int) -> str:
    """预约座位。date 格式 YYYY-MM-DD，time 格式 HH:MM，num_people 是人数。"""
    res_id = len(RESERVATIONS) + 1
    RESERVATIONS.append({"id": res_id, "date": date, "time": time, "people": num_people})
    return f"预约成功！预约号：{res_id}，{date} {time}，{num_people} 人。"
