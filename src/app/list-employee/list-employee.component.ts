import { Component, OnInit } from '@angular/core';
import {FormsModule} from '@angular/forms';             // for creating form
import {Employee} from './employee'
@Component({
  selector: 'app-list-employee',
  templateUrl: './list-employee.component.html',
  styleUrls: ['./list-employee.component.css']
})
export class ListEmployeeComponent implements OnInit {
  employees: Employee[] = [
    {
      employeeID: null,
      firstName: "string",
      lastName: "string",
      middleName: "string",
      ssn: 123456789,
      gender: "string",
      birthday: new Date(),
      email: "string@gmail.com",
      phoneNumber: 1,
      address: "string",
      hiringDate: new Date(),
      salary: 100000,
      position: "string",
    }

  ]
  constructor() { }

  ngOnInit() {
  }

}