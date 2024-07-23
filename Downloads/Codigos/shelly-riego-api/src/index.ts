// import express from 'express';
// import cors from 'cors';
// import { CONFIG } from './config/config';
// import { controlDeviceOutput } from './Api';

// const app = express();

// app.use(cors());
// app.use(express.json());

// app.post('/api/riego', async (req, res) => {
//   const { state } = req.body;
//   try {
//     const response = await controlDeviceOutput(state);
//     res.json(response);
//   } catch (error) {
//     console.error('Error al controlar el riego:', error);
//     res.status(500).json({ error: 'Error al controlar el riego' });
//   }
// });

// app.listen(CONFIG.port, () => {
//   console.log(`Servidor proxy corriendo en http://localhost:${CONFIG.port}`);
// });

import express from 'express';
import axios from 'axios';
import cors from 'cors';
import dotenv from 'dotenv';

dotenv.config();
import fs from 'fs';
import https from 'https';
import { CONFIG } from './config/config';
import { controlDeviceOutput } from './Api';

// Load SSL certificates
const sslOptions = {
  key: fs.readFileSync('/etc/letsencrypt/live/she.soursop.lat/privkey.pem'),
  cert: fs.readFileSync('/etc/letsencrypt/live/she.soursop.lat/fullchain.pem')
};

const app = express();
const port = process.env.PORT || 3080;
const SHELLY_IP = process.env.SHELLY_IP || '192.168.1.100'; // Asegúrate de configurar esto en tu archivo .env

app.use(cors());
app.use(express.json());

// Endpoint para toggle del relé
app.post('/api/riego', async (req, res) => {
  const { state } = req.body;
  try {
    const response = await axios.get(`http://${SHELLY_IP}/relay/0?turn=${state ? 'on' : 'off'}`);
    res.json(response.data);
  } catch (error) {
    console.error('Error al controlar el riego:', error);
    res.status(500).json({ error: 'Error al controlar el riego' });
  }
});

app.listen(port, () => {
  console.log(`Servidor proxy corriendo en http://localhost:${port}`);
});
// Create HTTPS server
https.createServer(sslOptions, app).listen(CONFIG.port, () => {
  console.log(`Servidor proxy corriendo en https://localhost:${CONFIG.port}`);
});
