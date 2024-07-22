import axios from 'axios';
import { CONFIG } from '../config/config';
import dotenv from 'dotenv';


dotenv.config();

export const checkDeviceStatus = async () => {
  const url = `http://${CONFIG.serverUri}/status`;
  try {
    const response = await axios.get(url);
    return response.data;
  } catch (error: unknown) {
    if (error instanceof Error) {
      throw new Error(`Error fetching device status: ${error.message}`);
    } else {
      throw new Error('Unknown error occurred');
    }
  }
};

export const controlDeviceOutput = async (state: boolean) => {
  const url = `http://${CONFIG.serverUri}/relay/0?turn=${state ? 'on' : 'off'}`;
  try {
    const response = await axios.get(url);
    return response.data;
  } catch (error: unknown) {
    if (error instanceof Error) {
      throw new Error(`Error controlling device output: ${error.message}`);
    } else {
      throw new Error('Unknown error occurred');
    }
  }
};

const SHELLY_LOCAL_IP = process.env.SHELLY_LOCAL_IP || '192.168.1.100';

export const getShellyStatus = async () => {
  try {
    const response = await axios.post(`http://${SHELLY_LOCAL_IP}/rpc/Shelly.GetStatus`, {});
    console.log('Estado del dispositivo:', response.data);
  } catch (error) {
    if (error instanceof Error) {
      console.error('Error al obtener el estado del dispositivo:', error.message);
    } else {
      console.error('Error desconocido al obtener el estado del dispositivo');
    }
  }
};
