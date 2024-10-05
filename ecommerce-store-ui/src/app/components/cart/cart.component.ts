import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-cart',
  templateUrl: './cart.component.html',
  styleUrls: ['./cart.component.scss']
})
export class CartComponent implements OnInit {
  cartItems: any[] = [];
  totalPrice: number = 0;

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.loadCart();
  }

  loadCart() {
    this.apiService.getCart().subscribe(cart => {
      this.cartItems = cart.items;
      this.totalPrice = this.cartItems.reduce((acc, item) => acc + item.product.price * item.quantity, 0);
    });
  }

  checkout() {
    this.apiService.checkout(null).subscribe(() => {
      alert('Order placed successfully!');
      this.cartItems = [];  // Clear cart
      this.totalPrice = 0;
    });
  }
}
