import express from 'express';
import cors from 'cors';
import fs from 'fs';
import https from 'https';
import { CONFIG } from './config/config';
import { controlDeviceOutput } from './Api';
import dotenv from 'dotenv';

// Load environment variables from .env file
dotenv.config();

// Load SSL certificates from environment variables
const sslOptions = {
  key: fs.readFileSync(process.env.SSL_KEY_PATH),
  cert: fs.readFileSync(process.env.SSL_CERT_PATH)
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
