import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Attach Token from localStorage if present
api.interceptors.request.use((config) => {
  try {
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers = config.headers || {}
      config.headers['Authorization'] = `Token ${token}`
    }
  } catch (_) {
    // ignore storage access issues
  }
  return config
})

export default api
