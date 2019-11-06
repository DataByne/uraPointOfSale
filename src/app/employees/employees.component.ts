import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { Employee } from './employee';

@Component({
  selector: 'app-employees',
  templateUrl: './employees.component.html',
  styleUrls: ['./employees.component.css']
})
export class EmployeesComponent implements OnInit {
  employees: Employee[] = [
    {
      employeeID: 1,
      firstName: "string",
      lastName: "string",
      middleName: "string",
      ssn: 123456789,
      gender: "string",
      birthday: new Date(),
      email: "string@gmail.com",
      phoneNumber: 1234567890,
      address: "string",
      hiringDate: new Date(),
      salary: 100000,
      position: "string",
    },
    {
      employeeID: 2,
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
  constructor(private router: Router) { }

  ngOnInit() {
  }

  editEmployee(employee){
    this.router.navigate(['/employees/edit', employee.employeeID]);
  }

  deleteEmployee(employee){
    if (confirm('Are you sure to delete this employee?') == true) {
      /* console.log("Implement delete functionality here") */
    }
  }


}
