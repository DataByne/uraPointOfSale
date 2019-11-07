import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { FormsModule } from '@angular/forms';

import { AppComponent } from './app.component';
import { FooterComponent } from './footer/footer.component';
import { HeaderComponent } from './header/header.component';
import { LandingComponent } from './landing/landing.component';
import { AboutComponent } from './about/about.component';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { EmployeesComponent } from './employees/employees.component';
import { EditEmployeeComponent } from './edit-employee/edit-employee.component';
import { ProductsComponent } from './products/products.component';
import { ProductComponent } from './product/product.component';
import { EditProductComponent } from './edit-product/edit-product.component';

const appRoutes: Routes = [

  { path: '', component: LandingComponent },
  { path: 'login' , component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'about' , component: AboutComponent },
  { path: 'employees', component: EmployeesComponent },
  { path: 'employees/add', component: EditEmployeeComponent },
  { path: 'employees/edit/:id', component: EditEmployeeComponent },
  { path: 'products', component:ProductsComponent},
  { path: 'products/add', component: EditProductComponent },
  { path: 'products/edit/:id', component: EditProductComponent },
  { path: 'products/:id', component: ProductComponent },
  { path: '**', redirectTo: '/', pathMatch: 'full' }];

@NgModule({
  declarations: [
    AppComponent,
    FooterComponent,
    HeaderComponent,
    LandingComponent,
    AboutComponent,
    LoginComponent,
    RegisterComponent,
    EmployeesComponent,
    EditEmployeeComponent,
    ProductsComponent,
    ProductComponent,
    EditProductComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    RouterModule.forRoot(appRoutes)
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }

