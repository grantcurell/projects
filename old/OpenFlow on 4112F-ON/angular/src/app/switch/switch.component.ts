import { Component, Input } from '@angular/core';
import { Subject } from 'rxjs';
import { Port, Port_role, Flow } from '../port'
import { UpdateportsService } from '../updateports.service';
import { MatDialog } from '@angular/material/dialog';
import { RedirectPopupComponent } from '../redirect-popup/redirect-popup.component';

@Component({
  selector: 'app-switch',
  templateUrl: './switch.component.html',
  styleUrls: ['./switch.component.css']
})
export class SwitchComponent {

  closeActive = new Subject<void>(); // TODO - look into this
  flows: Flow[];
  output_ports: number[];
  input_ports: number[];

  @Input() switchdpid: number;

  ngOnInit() {}

  ngOnDestroy() {
    this.closeActive.next();
    this.closeActive.complete();
  }

  _remove_old_value(port: Port): void {
    if (port["role"] == Port_role.input) {
      this.updateportsService.updatePorts(port, Port_role.input, "delete")
    } else if (port["role"] == Port_role.output) {
      this.updateportsService.updatePorts(port, Port_role.output, "delete")
    }
  }

  onButtonClick_InputPort(port: Port): void {
    this._remove_old_value(port);
    this.updateportsService.updatePorts(port, Port_role.input, "add");
    port.role = Port_role.input;
  }

  onButtonClick_OutputPort(port: Port): void {
    this._remove_old_value(port);
    this.updateportsService.updatePorts(port, Port_role.output, "add");
    port.role = Port_role.output;
  }

  onButtonClick_UnconfiguredPort(port: Port): void {
    this._remove_old_value(port)
    port.role = Port_role.unassigned;
  }

  openRedirectPortDialog() {
    this.updateportsService.getPorts();

    const dialogRef = this.dialog.open(RedirectPopupComponent,{
      /*Data to pass to dialog box would go here. You would need to update the constructor of RedirectPopupComponent*/
    });

    dialogRef.afterClosed().subscribe((confirmed: boolean) => {
      if (confirmed) {
        const a = document.createElement('a');
        a.click();
        a.remove();
      }
    });
  }

  constructor(public updateportsService: UpdateportsService, private dialog: MatDialog) {}

}
