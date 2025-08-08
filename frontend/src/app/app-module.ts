import { NgModule, provideBrowserGlobalErrorListeners } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { ReactiveFormsModule } from '@angular/forms';

import { AppRoutingModule } from './app-routing-module';
import { App } from './app';
import { Header } from './components/header/header';
import { Footer } from './components/footer/footer.component';
import { Hero } from './components/hero/hero.component';
import { About } from './components/about/about.component';
import { Services } from './components/services/services.component';
import { WhyUs } from './components/why-us/why-us.component';
import { Testimonials } from './components/testimonials/testimonials.component';
import { Blog } from './components/blog/blog.component';
import { Contact } from './components/contact/contact.component';

@NgModule({
  declarations: [
    App,
    Header,
    Footer,
    Hero,
    About,
    Services,
    WhyUs,
    Testimonials,
    Blog,
    Contact
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    ReactiveFormsModule
  ],
  providers: [
    provideBrowserGlobalErrorListeners()
  ],
  bootstrap: [App]
})
export class AppModule { }
