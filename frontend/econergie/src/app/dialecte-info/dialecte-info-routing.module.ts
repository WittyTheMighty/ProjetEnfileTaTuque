import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { DialecteInfoPage } from './dialecte-info.page';

const routes: Routes = [
  {
    path: '',
    component: DialecteInfoPage
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class DialecteInfoPageRoutingModule {}
