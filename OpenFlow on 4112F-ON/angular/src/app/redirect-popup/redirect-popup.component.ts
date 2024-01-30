import { Component, Inject } from '@angular/core';
import {FormControl, Validators, FormGroup, FormArray, FormBuilder} from '@angular/forms';
import { Port } from '../port'
import { UpdateportsService } from '../updateports.service';
import { map } from 'rxjs/operators';
import { BehaviorSubject } from 'rxjs';

@Component({
  selector: 'app-redirect-popup',
  templateUrl: './redirect-popup.component.html',
  styleUrls: ['./redirect-popup.component.css']
})
export class RedirectPopupComponent {
  redirectPortsForm: FormGroup;
  ports: Port[] = [];
  portsObservable$ = new BehaviorSubject(this.updateportsService.portsBehaviorSubject.getValue());
  redirectPortsFormControl = new FormControl('', [
    Validators.min(1),
    Validators.max(65535)
  ]);

  portsObserver = {
    next: ports => {
      this.configure_port_text(ports);
    }
  }

  constructor(private formBuilder: FormBuilder, public updateportsService: UpdateportsService) {
    this.ports = this.updateportsService.portsBehaviorSubject.getValue();

    this.redirectPortsForm = new FormGroup({
      redirectPortsArray: this.formBuilder.array([])
    });

    this.buildForm();
  }

  ngOnInit() {
    this.updateportsService.portsBehaviorSubject.subscribe(this.portsObserver);
  }

  configure_port_text(ports: Port[]): void {

    const controlArray = this.redirectPortsForm.get('redirectPortsArray') as FormArray;

    var redirect_text_entries: any[] = [];

    for (const [i, port] of ports.entries()) {

      if (port.redirects.length > 0) {
        
        port.redirect_text = "";

        for (let flow of port.redirects) {

          // TCP is nw_proto 6
          if (flow.match.nw_proto == 6 && flow.match.tp_dst !== undefined) {
            port.redirect_text += String(flow.match.tp_dst) + "/tcp,";

          // UDP is nw_proto 17
          } else if (flow.match.nw_proto == 17 && flow.match.tp_dst !== undefined) {
            port.redirect_text += String(flow.match.tp_dst) + "/udp,";
          } else if (flow.match.tp_src) {
            //nothing
          } else {
            console.log("Warning: This should never have been reached. This means \
             that we encountered an area where the server API sent an array of \
             port redirects, but that list had entries where the protocol wasn't\
              either 6 (TCP) or 17 (UDP). This should never happen! We are ignoring \
              the value.");
          }
        }

        // This just cuts off the last trailing ','
        port.redirect_text = port.redirect_text.substring(0, port.redirect_text.length - 1);
      } else {
        port.redirect_text = "";
      }

      controlArray.controls[i].patchValue({ port_entry: port.redirect_text });
    }

  }

  buildForm() {
    const controlArray = this.redirectPortsForm.get('redirectPortsArray') as FormArray;

    Object.keys(this.ports).forEach((i) => {
      controlArray.push(
        this.formBuilder.group({
          port_entry: new FormControl({ value: this.ports[i].redirect_text, disabled: false })
        })
      )
    })

    console.log(controlArray.controls)
  }

  updateSwitchRedirectPorts(i) {

    this.updateportsService.redirectPortSet(this.ports[i], this.redirectPortsForm.get('redirectPortsArray').get(i.toString()).value["port_entry"]);
    this.updateportsService.getPorts();
    
  }

  formControlState(i){
     const controlArray = this.redirectPortsForm.get('redirectPortsArray') as FormArray;
     return controlArray.controls[i].disabled
  }

}