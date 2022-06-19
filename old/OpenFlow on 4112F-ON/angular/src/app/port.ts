export interface Match {
  dl_type: number,
  nw_proto: number,
  tp_src?: number
  tp_dst?: number
}

// Flow received from the switch
export interface Flow { 
  priority: number,
  cookie: number,
  idle_timeout: number,
  hard_timeout: number,
  byte_count: number,
  duration_sec: number,
  duration_nsec: number,
  packet_count: number,
  length: number,
  flags: number,
  actions: {[key: string]: number},
  match: Match,
  table_id: number,
}

export interface Port {
    hw_addr: string
    name: string
    openflow_port: number
    role: Port_role
    redirects: Array<Flow>
    redirect_text?: string
}

// Used to store data on what an interface is currently doing
export enum Port_role { 
  input = "inport", 
  output = "outport", 
  unassigned = "unassigned"
}

// Set is not currently used, but it is a valid operation
export type Port_operation = "add" | "delete" | "set";