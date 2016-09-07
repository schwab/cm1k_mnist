import { provideRouter, RouterConfig } from '@angular/router';
import {Core} from './core';
import {AnotherPage} from './../another/another';
import {Dashboard} from './../dashboard/dashboard';

export const CoreRoutes: RouterConfig = [
  {
    path: 'app',
    component: Core,
    children: [
      { path: 'dashboard', component: Dashboard},
      { path: 'another-page', component: AnotherPage}
    ]
  }
];
