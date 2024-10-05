import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-product-list',
  templateUrl: './product-list.component.html',
  styleUrls: ['./product-list.component.scss']
})
export class ProductListComponent implements OnInit {
  previousOrders: any[] = [];
  products:any = [];
  cart: { [key: number]: number } = {};
  totalItemsInCart: number = 0;

  constructor(private apiService: ApiService) {}

  ngOnInit() {
    this.apiService.getProducts().subscribe((response: any) => {
      this.products = response;
    });

    this.loadCart();
    this.loadPreviousOrders();
  }

  loadPreviousOrders() {
    this.apiService.getOrderHistory().subscribe((orders: any) => {
      this.previousOrders = orders;
    });
  }

  addToCart(product: any) {
    this.cart[product.id] = (this.cart[product.id] || 0) + 1;
    this.apiService.addItemToCart(product.id, 1).subscribe(() => {
      this.loadCart();
    });
  }

  loadCart() {
    this.apiService.getCart().subscribe((cart: any) => {
      this.cart = cart.items.reduce((acc: any, item: any) => {
        acc[item.product.id] = item.quantity;
        return acc;
      }, {});
      this.totalItemsInCart = Object.values(this.cart).reduce((acc: number, qty: any) => acc + qty, 0);
    });
  }
}
