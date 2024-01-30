import { Port } from './port'

export interface Switch {
    datapath: number
    name: string
    ports: Array<Port>[]
}