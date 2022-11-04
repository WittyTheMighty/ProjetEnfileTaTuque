import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { DialecteInfoPageRoutingModule } from './dialecte-info-routing.module';

import { DialecteInfoPage } from './dialecte-info.page';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    DialecteInfoPageRoutingModule
  ],
  declarations: [DialecteInfoPage]
})
export class DialecteInfoPageModule {}
