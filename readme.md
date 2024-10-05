# Ecommerce Web Application

This project is a full-stack e-commerce application with both frontend (Angular) and backend (Django). It provides the functionalities of product listing, cart management, checkout, and order history. This README will give you a brief technical overview of the project structure, key components, and setup instructions.

# Project Structure

### Frontend (Angular)
```
|-- package-lock.json
|-- package.json
|-- src
|   |-- app
|   |   |-- components (contains login, product list, and cart components)
|   |   |-- guards (contains auth guards for route protection)
|   |   |-- services (contains API service for interacting with backend)
|   |-- assets (contains static assets)
|   |-- environment (contains environment variables for API base URLs)
|   |-- favicon.ico (favicon for the website)
|   |-- index.html (entry point for Angular app)
|   |-- main.ts (main TypeScript file for bootstrapping the Angular app)
|   |-- styles.scss (global SCSS file for custom styles)
|-- tsconfig.app.json (TypeScript configuration for the app)
|-- tsconfig.json (global TypeScript configuration)
|-- tsconfig.spec.json (TypeScript configuration for testing)
```
### Backend (Django)
```
|-- ecommerce_store (Main Django project directory)
|   |-- settings.py (Main configuration file for the Django application)
|   |-- urls.py (Routes for the Django application)
|   |-- wsgi.py (WSGI configuration for deployment)
|-- manage.py (Command-line utility for managing the Django project)
|-- orders (Django app responsible for handling orders and checkout)
|   |-- models.py (Order and OrderItem models)
|   |-- serializers.py (Serializers for order-related APIs)
|   |-- views.py (Views to handle order-related operations)
|-- products (Django app responsible for managing products)
|   |-- models.py (Product and Category models)
|   |-- serializers.py (Serializers for product-related APIs)
|   |-- views.py (Views to handle product-related operations)
|-- requirements.txt (Contains Python dependencies)
|-- venv (Virtual environment for the backend)

```

### Frontend Details

Key Features:
1. Login Page: Users can log in using their credentials.
2. Product Listing: Displays products in a grid format. Each product can be added to the cart.
3. Cart: Shows items added to the cart with total price and quantity.
4. Checkout: Allows users to place an order.
5. Order History: Displays a list of previous orders placed by the user.

Key Components:
1. LoginComponent: Handles user login and authentication.
2. ProductListComponent: Displays the list of available products and includes the "Add to Cart" functionality.
3. CartComponent: Displays the items in the cart and allows users to proceed to checkout.
4. AuthGuard: Protects routes that require authentication, such as the product list and cart.

### Backend Details
Key Features:
1. Product Management: APIs for retrieving product listings.
2. Order Management: APIs for placing orders, viewing order history, and managing carts.
3. Django Rest Framework (DRF): Used for building the RESTful APIs for the frontend to interact with.

Key Applications:
1. Products App: Manages the products available for purchase. It includes models for products and categories.
2. Orders App: Manages the user's cart, order placement, and order history.

## Setup Instructions

### Backend Setup (Django)

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Migrate the database**:
   ```bash
   python manage.py migrate
   ```
3. **Run the development server**:
   ```bash
   python manage.py runserver
   ```
4. **API Endpoint**:
   ```bash
   /api-token-auth/: Login endpoint.
   /products-api/products/: Get all products.
   /orders-api/checkout/: Checkout and place an order.
   /orders-api/order-history/: Get previous orders.
   ```

### Frontend Setup (Angular)

1. **Install dependencies**:
   ```bash
   npm install
   ```
2. **Run the development server**:
   ```bash
   ng serve
   ```
3. **Environment Configuration: Set the apiUrl in src/environment/environment.ts to point to your Django backend URL.**:
   ```bash
   export const environment = {
      production: false,
      apiUrl: 'http://127.0.0.1:8000'
    };
   ```

## Key Technical Notes
1. **Frontend**: Uses Angular Material for UI components. SCSS is used for styling.
2. **Backend**: Uses Django Rest Framework for API building. Models are linked using ForeignKey relationships.
3. **API Service**: The frontend communicates with the backend through a centralized API service in Angular (ApiService).
4. **Auth Guards**: Protects routes from unauthorized access.

This documentation provides a high-level overview of the technical structure of this project. For more details, explore each app’s respective files and review the comments within the code.
