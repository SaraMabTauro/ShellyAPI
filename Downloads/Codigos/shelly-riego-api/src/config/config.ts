import dotenv from 'dotenv';

dotenv.config();

export const CONFIG = {
  serverUri: process.env.SHELLY_IP || '192.168.1.93',
  deviceId: process.env.SHELLY_ID || '3494547af54b',
  authKey: process.env.SHELLY_AUTH_KEY || 'MjYxZmZhdWlk877182A1E82777613788391AB098AD4022A4ECDF8F66EEF41F36E4BDD9D01C1377546216F0DA89D5',
  port: process.env.PORT || 3080
};
