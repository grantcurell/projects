import { Component } from '@angular/core';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';
import { Observable } from 'rxjs';
import { map, shareReplay } from 'rxjs/operators';
import { UpdateportsService } from '../updateports.service';
import { FormControl, Validators } from '@angular/forms';
import { HttpErrorResponse } from '@angular/common/http';
import { Port } from '../port';

// Regular Expression for a URL
const reg = '^(ht|f)tp(s?)\:\/\/[0-9a-zA-Z]([-.\w]*[0-9a-zA-Z])*(:(0-9)*)*(\/?)([a-zA-Z0-9\-\.\?\,\'\/\\\+&amp;%\$#_]*)?$';

@Component({
  selector: 'app-managedswitches',
  templateUrl: './managedswitches.component.html',
  styleUrls: ['./managedswitches.component.css']
})
export class ManagedswitchesComponent {

  switches: number[] = [];  // Contains a list of DPIDs one for each switch
  controllerAddress: string;  // The address of the OpenFlow controller
  controllerValidated: boolean = false;  // Whether or not the entered controller IP has passed validation
  controllerTestFailed: boolean = false;  // If the entered IP has failed a connection test this is true
  controllerError: HttpErrorResponse;  // The error returned during the connection test.
  switchSelected: boolean = false;  // Whether or not the user has selected a switch in the menu on the left
  ports: Port[];

  public portsObserver = {
    next: x => console.log(x),
    error: err => console.error('Ports observer got an error: ' + err),
    complete: () => {
      console.log('Received all ports from switch.');
    },
  };

  switchesObserver = {
    next: x => {
      if (x.length < 1) {
        this.controllerTestFailed = true;
        this.controllerValidated = false;
        this.switches = [];    
      } else {
        this.switches = x;
        this.controllerError = undefined;
        this.controllerTestFailed = false;
        this.controllerValidated = true;
      }
    },
    error: err => {
      this.controllerTestFailed = true;
      this.controllerValidated = false; 
      this.controllerError = err;
      this.switches = [];
    },
    complete: () => { 
      if (!this.controllerTestFailed) {
        this.controllerValidated = true; 
        this.controllerTestFailed = false; 
        console.log("Controller test succeeded! We received all the switches from the server!");
      } else {
        console.log("Something went wrong during the controller test!")
      }},
  };

  controllerAddressFormControl = new FormControl('', [
    Validators.required,
    Validators.pattern(reg),
  ]);

  isHandset$: Observable<boolean> = this.breakpointObserver.observe(Breakpoints.Handset)
    .pipe(
      map(result => result.matches),
      shareReplay()
    );

  testConnection() {
    this.controllerAddress = this.controllerAddressFormControl.value;
    this.updateportsService.setControllerIp(this.controllerAddress)
    console.log("Entered controller address is: " + this.controllerAddress)

    // All this does is run getPorts and then check to see if there is any valid
    // response.
    this.updateportsService.getSwitches().subscribe(this.switchesObserver);
  }

  selectSwitch(i: number): void {
    this.updateportsService.setSelectedDpid(this.switches[i]);
    this.switchSelected = true;
  }

  ngOnInit() {}

  constructor(private breakpointObserver: BreakpointObserver, public updateportsService: UpdateportsService) {}

}
