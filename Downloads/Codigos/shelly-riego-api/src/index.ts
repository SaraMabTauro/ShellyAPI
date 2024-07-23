import express from 'express';
import axios from 'axios';
import cors from 'cors';
import dotenv from 'dotenv';
import fs from 'fs';
import https from 'https';

dotenv.config();
import { CONFIG } from './config/config';

const app = express();
const port = process.env.PORT || CONFIG.port;  // Usa CONFIG.port o el puerto de entorno
const SHELLY_IP = process.env.SHELLY_IP || '192.168.1.100'; // Asegúrate de configurar esto en tu archivo .env

// Load SSL certificates
const sslOptions = {
  key: fs.readFileSync('/etc/letsencrypt/live/shell.soursop.lat/privkey.pem'),
  cert: fs.readFileSync('/etc/letsencrypt/live/shell.soursop.lat/fullchain.pem')
};

// Configure CORS
app.use(cors({
  origin: '*', // Permite solicitudes desde este origen
  methods: ['GET', 'POST'],
  allowedHeaders: ['Content-Type']
}));

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

https.createServer(sslOptions, app).listen(port, () => {
  console.log(`Servidor proxy corriendo en https://localhost:${port}`);
});
