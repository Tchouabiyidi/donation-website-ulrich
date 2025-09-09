import axios from 'axios'

// Smart API configuration that detects environment
function getApiBaseUrl() {
  // Highest priority: explicit env var from Vite/Render
  if (import.meta?.env?.VITE_API_BASE_URL) {
    return import.meta.env.VITE_API_BASE_URL
  }

  // Determine if running locally
  const host = typeof window !== 'undefined' ? window.location.hostname : ''
  const isLocalhost = host === 'localhost' || host === '127.0.0.1' || host === '0.0.0.0'
  const isDevelopment = !!import.meta?.env?.DEV

  // Use local backend only when in dev AND on localhost
  if (isDevelopment && isLocalhost) {
    return 'http://127.0.0.1:8000/api'
  }

  // Production default (Render backend)
  return 'https://donation-website-ulrich.onrender.com/api'
}

const api = axios.create({
  baseURL: getApiBaseUrl(),
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
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

// Response interceptor for 401 handling (optional)
api.interceptors.response.use(
  (res) => res,
  (error) => {
    if (error?.response?.status === 401) {
      try { localStorage.removeItem('auth_token') } catch (_) {}
      // Optionally redirect to login
      // if (typeof window !== 'undefined') window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export const getCurrentApiUrl = () => getApiBaseUrl()
export default api
