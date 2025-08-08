import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private apiUrl = 'http://localhost:8000'; // URL to the Python backend

  constructor(private http: HttpClient) { }

  sendContactRequest(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/contact`, data);
  }
}
