import { exec } from 'child_process';

export const findShellyIp = (deviceId: string): Promise<string | null> => {
  return new Promise((resolve, reject) => {
    exec('nmap -sn 192.168.1.0/24', (error, stdout, stderr) => {
      if (error) {
        reject(error);
      } else {
        const ipMatch = stdout.match(new RegExp(`(${deviceId})\\s*\\((.*?)\\)`, 'i'));
        if (ipMatch && ipMatch[2]) {
          resolve(ipMatch[2]);
        } else {
          resolve(null);
        }
      }
    });
  });
};
