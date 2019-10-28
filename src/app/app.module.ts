import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { AppComponent } from './app.component';
import { FooterComponent } from './footer/footer.component';
import { HeaderComponent } from './header/header.component';
import { LandingPageComponent } from './landing-page/landing-page.component';
import { AboutPageComponent } from './about-page/about-page.component';
import { LoginPageComponent } from './login-page/login-page.component';
import { RegisterPageComponent } from './register-page/register-page.component';
import { InsertEmployeeComponent } from './insert-employee/insert-employee.component';
import { ListEmployeeComponent } from './list-employee/list-employee.component';
import { EditEmployeeComponent } from './edit-employee/edit-employee.component';

const appRoutes: Routes = [
  { path:'landing', component:LandingPageComponent },
  { path:'login' , component:LoginPageComponent },
  { path:'registration', component:RegisterPageComponent },
  { path:'about' , component:AboutPageComponent },
  { path:'insert_employee', component:InsertEmployeeComponent },
  { path:'list_employee', component:ListEmployeeComponent },
  { path:'edit_employee', component:EditEmployeeComponent},
  { path: '', redirectTo:'landing',pathMatch:'full'},
  { path:'**', component:LandingPageComponent}
];

@NgModule({
  declarations: [
    AppComponent,
    FooterComponent,
    HeaderComponent,
    LandingPageComponent,
    AboutPageComponent,
    LoginPageComponent,
    RegisterPageComponent,
    InsertEmployeeComponent,
    ListEmployeeComponent,
    EditEmployeeComponent
  ],
  imports: [
    BrowserModule,
    RouterModule.forRoot(appRoutes)
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
