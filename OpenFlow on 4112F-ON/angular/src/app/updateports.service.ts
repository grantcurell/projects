import { Injectable } from '@angular/core';
import { Port, Port_role, Port_operation, Flow } from './port'
import { Observable, of, BehaviorSubject } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class UpdateportsService {

  public dpid: number;
  private app_name = 'gelante';
  private controller_ip: string;
  private getports_url: string;
  private inports_url: string;
  private outports_url: string;
  private redirectports_url: string;
  private getswitches_url: string;
  private flows_url: string;
  public portsBehaviorSubject = new BehaviorSubject<Port[]>([]);

  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };

  /**
   * Allows you to set the IP address of the controller you wish to use
   * 
   * @param controller_ip - The IP address of the controller
   */
  setControllerIp(controller_ip: string): void {
    this.controller_ip = controller_ip;
    this.getswitches_url = this.controller_ip + "/" + this.app_name + "/ryuapi/stats/switches"
  }

  setSelectedDpid(dpid: number): void {
    this.dpid = dpid;
    this.getports_url = this.controller_ip + '/' + this.app_name + '/getports/' + this.dpid;
    this.inports_url = this.controller_ip + '/' + this.app_name + '/inports/' + this.dpid;
    this.outports_url = this.controller_ip + '/' + this.app_name + '/outports/' + this.dpid;
    this.redirectports_url = this.controller_ip + '/' + this.app_name + '/redirectport/' + this.dpid;
    this.flows_url = this.controller_ip + "/" + this.app_name + "/ryuapi/flow/" + this.dpid;
    this.getPorts();
  }

  /**
   * Handle Http operation that failed.
   * Let the app continue.
   * @param operation - name of the operation that failed
   * @param result - optional value to return as the observable result
   */
  private handleError<T>(operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {

      console.error(error); // log to console instead

      // Let the app keep running by returning an empty result.
      return of(result as T);
    };
  }

    /**
   * getPorts reaches out to the switch and gets a listing of all of its current
   * ports.
   * 
   * @remarks Port_with_colrow exists to allow granular control of the width of
   *          the port's card in the display. I currently have this value fixed
   *          but in the future could extend it to allow more dynamic control.
   *
   * @returns An array containing all of the ports from the switch. See ports.ts
   *          for details on the format of the Port object.
   */
  getPorts(): void {
    this.http.get<Port[]>(this.getports_url).subscribe(ports => {
      this.portsBehaviorSubject.next(ports);
    });
  }

  //curl -X PUT -d '{"operation": "set", "<tcp_port|udp_port>" : [1,2,3,4,5,6], "out_port" : <openflow_port>}' http://127.0.0.1:8080/gelante/redirectport/150013889525632
  redirectPortSet(port: Port, redirect_ports: String): void {
    this.http.put(this.redirectports_url, {"out_port": port["openflow_port"], "operation": "set", "ports": redirect_ports}, this.httpOptions).subscribe(res => {console.log(res);});
  }

  /**
   * This function reaches out to the switch and updates the port configuration.
   *
   * @param port - The port on which you want to perform the operation
   * @param portType - The ports current type. This could be input, output, or unassigned
   * @returns Nothing
   */
  updatePorts(port: Port, portType: Port_role, operation: Port_operation): void {

    if (portType == Port_role.output) {
      this.http.put(this.outports_url, {"openflow_port": port["openflow_port"], "operation": operation}, this.httpOptions).subscribe(res => {console.log(res);});
    } else if (portType == Port_role.input) {
      this.http.put(this.inports_url, {"openflow_port": port["openflow_port"], "operation": operation}, this.httpOptions).subscribe(res => {console.log(res);});
    } else {
      console.log("It looks like updatePorts was passed an invalid portType!")
    }

  }

  getFlows(): Observable<Flow[]> {
    return this.http.get<Flow[]>(this.flows_url)
  }

  getSwitches(): Observable<number[]> {    
    return this.http.get<number[]>(this.getswitches_url)
  }

  getOutports(): Observable<number[]> {    
    return this.http.get<number[]>(this.outports_url)
  }

  getInports(): Observable<number[]> {    
    return this.http.get<number[]>(this.inports_url)
  }

  constructor(private http: HttpClient) { }
}
