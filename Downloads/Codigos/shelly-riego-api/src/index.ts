import express from 'express';
import cors from 'cors';
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

app.use(cors());
app.use(express.json());

app.post('/api/riego', async (req, res) => {
  const { state } = req.body;
  try {
    const response = await controlDeviceOutput(state);
    res.json(response);
  } catch (error) {
    console.error('Error al controlar el riego:', error);
    res.status(500).json({ error: 'Error al controlar el riego' });
  }
});

// Create HTTPS server
https.createServer(sslOptions, app).listen(CONFIG.port, () => {
  console.log(`Servidor proxy corriendo en https://localhost:${CONFIG.port}`);
});
