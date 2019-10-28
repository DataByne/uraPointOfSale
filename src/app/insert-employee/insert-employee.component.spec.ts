import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { InsertEmployeeComponent } from './insert-employee.component';

describe('InsertEmployeeComponent', () => {
  let component: InsertEmployeeComponent;
  let fixture: ComponentFixture<InsertEmployeeComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ InsertEmployeeComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(InsertEmployeeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
