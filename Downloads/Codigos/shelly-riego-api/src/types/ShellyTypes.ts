export interface DeviceStatus {
    isok: boolean;
    data: {
      online: boolean;
      device_status: any;
    };
}
  
export interface ControlResponse {
    isok: boolean;
    data: any;
}
  