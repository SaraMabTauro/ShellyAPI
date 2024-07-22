import express from 'express';
import cors from 'cors';
import { CONFIG } from './config/config';
import { controlDeviceOutput } from './Api';

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

app.listen(CONFIG.port, () => {
  console.log(`Servidor proxy corriendo en http://localhost:${CONFIG.port}`);
});