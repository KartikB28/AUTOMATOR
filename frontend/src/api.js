import axios from 'axios';

let BASE_URL = 'http://localhost:8765';

async function initBaseUrl() {
  if (typeof window !== 'undefined' && window.electron) {
    try {
      const port = await window.electron.getPythonPort();
      BASE_URL = `http://localhost:${port}`;
    } catch (e) {
      console.error('Failed to get Python port:', e);
    }
  }
}

initBaseUrl();

const api = axios.create({ timeout: 30000 });

api.interceptors.request.use(config => {
  config.baseURL = BASE_URL;
  return config;
});

api.interceptors.response.use(
  r => r.data,
  err => Promise.reject(err.response?.data || err.message)
);

export const bots = {
  getStatus: () => api.get('/api/bots/status'),
  trigger: (name) => api.post(`/api/bots/${name}/trigger`),
  pause: (name) => api.post(`/api/bots/${name}/pause`),
  resume: (name) => api.post(`/api/bots/${name}/resume`),
  pauseAll: () => api.post('/api/bots/pause-all'),
  resumeAll: () => api.post('/api/bots/resume-all'),
  getRuns: (botName, limit = 50) => api.get('/api/bots/runs', { params: { bot_name: botName, limit } }),
};

export const content = {
  list: (params) => api.get('/api/content/', { params }),
  get: (id) => api.get(`/api/content/${id}`),
  update: (id, data) => api.patch(`/api/content/${id}`, data),
  delete: (id) => api.delete(`/api/content/${id}`),
  stats: () => api.get('/api/content/stats/summary'),
};

export const niches = {
  list: () => api.get('/api/niches/'),
  create: (data) => api.post('/api/niches/', data),
  get: (id) => api.get(`/api/niches/${id}`),
  update: (id, data) => api.patch(`/api/niches/${id}`, data),
  delete: (id) => api.delete(`/api/niches/${id}`),
};

export const analytics = {
  overview: (days = 30) => api.get('/api/analytics/overview', { params: { days } }),
  digest: () => api.get('/api/analytics/digest'),
  timeseries: (metric, days, platform) =>
    api.get('/api/analytics/timeseries', { params: { metric, days, platform } }),
};

export const schedule = {
  get: (nicheId) => api.get(`/api/schedule/${nicheId}`),
  create: (data) => api.post('/api/schedule/', data),
  delete: (id) => api.delete(`/api/schedule/${id}`),
  toggle: (id) => api.patch(`/api/schedule/${id}/toggle`),
};

export const settings = {
  get: () => api.get('/api/settings/'),
  getEnvPath: () => api.get('/api/settings/env-path'),
};

export const system = {
  health: () => api.get('/api/system/health'),
  stats: () => api.get('/api/system/stats'),
};

export const getMediaUrl = (path) => {
  if (!path) return null;
  if (path.startsWith('http')) return path;
  const parts = path.split('/media/');
  if (parts.length > 1) return `${BASE_URL}/media/${parts[parts.length - 1]}`;
  return `${BASE_URL}/media/${path.split('/').pop()}`;
};
