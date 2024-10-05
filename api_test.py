import requests

BASE_URL = "http://127.0.0.1:8000"
USERNAME = "pritish"
PASSWORD = "12345678"


def login():
    # Login using token authentication
    print("Logging in with token authentication...")
    response = requests.post(f"{BASE_URL}/api-token-auth/", data={"username": USERNAME, "password": PASSWORD})
    if response.status_code == 200:
        token = response.json().get("token")
        print(f"Logged in. Token: {token}")
        return token
    else:
        print("Login failed!")
        return None


def list_products(session, token):
    # List all products
    print("\nListing products...")
    headers = {"Authorization": f"Token {token}"}
    response = session.get(f"{BASE_URL}/products-api/products/", headers=headers)
    print(response.json())


def add_item_to_cart(session, token):
    # Add an item to the cart
    print("\nAdding item to cart...")
    data = {
        "product_id": 1,  # Assuming product with ID 1 exists
        "quantity": 2
    }
    headers = {"Authorization": f"Token {token}"}
    response = session.post(f"{BASE_URL}/cart-api/add/", json=data, headers=headers)
    print(response.json())


def get_cart(session, token):
    # Get the current cart for the user
    print("\nGetting cart details...")
    headers = {"Authorization": f"Token {token}"}
    response = session.get(f"{BASE_URL}/cart-api/", headers=headers)
    print(response.json())


def checkout(session, token, discount_code=None):
    # Checkout with or without a discount code
    print("\nChecking out...")
    data = {"discount_code": discount_code} if discount_code else {}
    headers = {"Authorization": f"Token {token}"}
    response = session.post(f"{BASE_URL}/orders-api/checkout/", json=data, headers=headers)
    print(response.json())


def order_history(session, token):
    # Fetch the user's order history
    print("\nFetching order history...")
    headers = {"Authorization": f"Token {token}"}
    response = session.get(f"{BASE_URL}/orders-api/order-history/", headers=headers)
    print(response.json())


def run_all():
    # Create a session
    session = requests.Session()

    # Login and get token
    token = login()

    if token:
        # List products
        list_products(session, token)

        # Add an item to the cart
        add_item_to_cart(session, token)

        # Get the current cart
        get_cart(session, token)

        # Checkout without discount
        checkout(session, token)

        # Checkout with discount code
        checkout(session, token, discount_code="DISCOUNT5")

        # Fetch order history
        order_history(session, token)


if __name__ == "__main__":
    run_all()
