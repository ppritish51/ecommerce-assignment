import { Component } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent {
  username = '';
  password = '';

  constructor(private apiService: ApiService, private router: Router) {}

  login() {
    this.apiService.login(this.username, this.password).subscribe(
      (response) => {
        if (response.token) {
          localStorage.setItem('authToken', response.token);
          this.router.navigate(['/products']);
        } else {
          alert('Login failed!');
        }
      },
      (error) => {
        alert('Login failed!');
      }
    );
  }
}
