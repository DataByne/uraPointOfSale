import { Component, OnInit} from '@angular/core';
import { Product } from '../product';
import { ProductService } from '../product.service';

import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';

@Component({
  selector: 'app-product',
  templateUrl: './product.component.html',
  styleUrls: ['./product.component.css']
})
export class ProductComponent implements OnInit {

  product: Product;

  constructor(
    private route: ActivatedRoute,
    private productService: ProductService,
    private location: Location
  ) {
  }

  ngOnInit() {
    this.getProduct();
  }

  getProduct() {
    const id = +this.route.snapshot.paramMap.get('product_id');
    this.productService.getProduct(id).subscribe(product => this.product = product);
  }

  goBack() {
    this.location.back();
  }

}
