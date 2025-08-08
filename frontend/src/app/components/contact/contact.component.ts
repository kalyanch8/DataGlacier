import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-contact',
  templateUrl: './contact.component.html',
  styleUrls: ['./contact.component.css']
})
export class Contact implements OnInit {
  contactForm: FormGroup;
  isSubmitting = false;
  submissionStatus: 'success' | 'error' | null = null;

  constructor(
    private fb: FormBuilder,
    private apiService: ApiService
  ) { }

  ngOnInit(): void {
    this.contactForm = this.fb.group({
      name: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      service: ['Web Development', Validators.required],
      message: ['', Validators.required]
    });
  }

  onSubmit(): void {
    if (this.contactForm.invalid) {
      return;
    }

    this.isSubmitting = true;
    this.submissionStatus = null;

    this.apiService.sendContactRequest(this.contactForm.value).subscribe({
      next: () => {
        this.submissionStatus = 'success';
        this.isSubmitting = false;
        this.contactForm.reset({
          service: 'Web Development' // Reset with default value
        });
      },
      error: () => {
        this.submissionStatus = 'error';
        this.isSubmitting = false;
      }
    });
  }
}
