/*
 * Providers provided by Angular
 */

import 'jquery';
import 'tether';
import 'bootstrap';
import 'widgster';
import 'jquery-touchswipe/jquery.touchSwipe';
import 'jquery-slimscroll/jquery.slimscroll';
import 'pace';
import {enableProdMode} from '@angular/core';
import {bootstrap} from '@angular/platform-browser-dynamic';
import {LocationStrategy, HashLocationStrategy} from '@angular/common';
import {HTTP_PROVIDERS} from '@angular/http';
import {APP_ROUTER_PROVIDERS} from './app.routes';

const ENV_PROVIDERS = [];

if ('production' === process.env.ENV) {
  enableProdMode();
}

import {App} from './app';
import {ConfigService} from './app/core/config';

document.addEventListener('DOMContentLoaded', function main(): void {
  bootstrap(App, [
    ConfigService,
    ...ENV_PROVIDERS,
    ...HTTP_PROVIDERS,
    ...APP_ROUTER_PROVIDERS,
    {provide: LocationStrategy, useClass: HashLocationStrategy }
  ])
  .catch(err => console.error(err));
});
