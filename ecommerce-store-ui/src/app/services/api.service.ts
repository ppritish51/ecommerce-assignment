import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from 'src/environment/environment';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private baseUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  // Check if the user is authenticated (i.e., if a token exists in localStorage)
  isAuthenticated(): boolean {
    return !!localStorage.getItem('authToken');
  }

  // Login API
  login(username: string, password: string): Observable<any> {
    return this.http.post<any>(`${this.baseUrl}/api-token-auth/`, { username, password });
  }

  // Get all products
  getProducts(): Observable<any> {
    return this.http.get<any>(`${this.baseUrl}/products-api/products/`);
  }

  // Add item to cart
  addItemToCart(productId: number, quantity: number): Observable<any> {
    return this.http.post<any>(`${this.baseUrl}/cart-api/add/`, { product_id: productId, quantity });
  }

  // Get cart details
  getCart(): Observable<any> {
    return this.http.get<any>(`${this.baseUrl}/cart-api/`);
  }

  // Checkout
  checkout(discountCode: string | null): Observable<any> {
    const data = discountCode ? { discount_code: discountCode } : {};
    return this.http.post<any>(`${this.baseUrl}/orders-api/checkout/`, data);
  }

  // Get order history
  getOrderHistory(): Observable<any> {
    return this.http.get<any>(`${this.baseUrl}/orders-api/order-history/`);
  }
}
