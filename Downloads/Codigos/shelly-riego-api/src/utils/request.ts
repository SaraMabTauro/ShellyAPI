import axios, { AxiosResponse } from 'axios';

export const postRequest = async <T>(url: string, data: any): Promise<AxiosResponse<T>> => {
  return axios.post<T>(url, new URLSearchParams(data), {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  });
};
