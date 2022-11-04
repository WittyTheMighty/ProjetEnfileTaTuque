import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ChallengeService {
  baseUrl = 'http://localhost:8080/api/'
  constructor(private http:HttpClient) { }

  getChallenges(){
    this.http.get(this.baseUrl+'challenges/')
  }
}
