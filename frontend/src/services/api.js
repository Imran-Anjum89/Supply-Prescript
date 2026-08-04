import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor to add JWT Auth Token to outgoing requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => Promise.reject(error));

export const authAPI = {
  login: (data) => api.post('/auth/login', data),
  register: (data) => api.post('/auth/register', data),
  getMe: () => api.get('/auth/me'),
};

export const shipmentAPI = {
  list: () => api.get('/shipments'),
  get: (id) => api.get(`/shipment/${id}`),
  create: (data) => api.post('/shipment', data),
  update: (id, data) => api.put(`/shipment/${id}`, data),
  delete: (id) => api.delete(`/shipment/${id}`),
};

export const supplierAPI = {
  list: () => api.get('/suppliers'),
  create: (data) => api.post('/suppliers', data),
};

export const predictionAPI = {
  predict: (shipment_id) => api.post('/predict', { shipment_id }),
  getHistory: (shipment_id) => api.get(`/predictions/shipment/${shipment_id}`),
};

export const optimizationAPI = {
  recommend: (shipment_id, max_budget_extra = 1200) => api.post('/recommend', { shipment_id, max_budget_extra }),
  getHistory: (shipment_id) => api.get(`/recommendations/shipment/${shipment_id}`),
};

export const decisionAPI = {
  submit: (recommendation_id, action_taken, override_reason = null) =>
    api.post('/decision', { recommendation_id, action_taken, override_reason }),
  getHistory: (limit = 50) => api.get(`/history?limit=${limit}`),
};

export const feedbackAPI = {
  submit: (decision_id, actual_delay_days, actual_extra_cost = 0, outcome_rating = 5, notes = '') =>
    api.post('/feedback', { decision_id, actual_delay_days, actual_extra_cost, outcome_rating, notes }),
};

export const analyticsAPI = {
  getDashboard: () => api.get('/dashboard'),
  getAnalytics: () => api.get('/analytics'),
};

export const retrainingAPI = {
  trigger: () => api.post('/retrain'),
  getLogs: () => api.get('/retrain/logs'),
  getModelStatus: () => api.get('/model/evaluation'),
};

export default api;
