import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http'

@Injectable()
export class AuthService {
    baseUrl = 'http://localhost:8080/api/auth/'

    constructor(private http:HttpClient) {}

  register(form: any) {
        console.log(form)
        return this.http.post(this.baseUrl + 'register', form);
  }
  login(form: any) {
    console.log(form)
    return this.http.post(this.baseUrl + 'login', form);
}


}