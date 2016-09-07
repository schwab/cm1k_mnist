import {Component} from '@angular/core';
import {Http, HTTP_PROVIDERS} from '@angular/http';
import {Widget} from '../core/widget/widget';

@Component({
  selector: 'dashboard',
  template: require('./dashboard.html'),
  directives: [Widget]
})

export class Dashboard {
  data =  [];
  constructor(http :Http)
  {
    http.get('trainingRuns.json')
        .map(res => res.json())
        .subscribe(data => {this.data = data; console.log("Got Data",data);},
                    err => console.log(err),
                    () => console.log('Completed'));
  }
  getImageList()
  {

  }
}
