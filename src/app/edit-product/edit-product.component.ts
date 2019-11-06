import { Component, OnInit} from '@angular/core';
import { Product } from '../product';
import { ProductService } from '../product.service';

import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';

@Component({
  selector: 'app-edit-product',
  templateUrl: './edit-product.component.html',
  styleUrls: ['./edit-product.component.css']
})
export class EditProductComponent implements OnInit {

  constructor(private location: Location) { }

  goBack() {
    this.location.back();
  }

  ngOnInit() {
  }

}
