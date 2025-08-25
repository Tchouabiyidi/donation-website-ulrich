import { defineStore } from 'pinia'
import api from '../lib/api'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: null,
    user: null,
    loading: false,
    error: null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
  },

  actions: {
    loadFromStorage() {
      const token = localStorage.getItem('auth_token')
      const user = localStorage.getItem('auth_user')
      this.token = token || null
      this.user = user ? JSON.parse(user) : null
    },

    _saveSession(token, user) {
      this.token = token
      this.user = user
      localStorage.setItem('auth_token', token)
      localStorage.setItem('auth_user', JSON.stringify(user))
    },

    _clearSession() {
      this.token = null
      this.user = null
      localStorage.removeItem('auth_token')
      localStorage.removeItem('auth_user')
    },

    async register(payload) {
      this.loading = true
      this.error = null
      try {
        const { data } = await api.post('/users/register/', payload)
        this._saveSession(data.token, data.user)
        return data
      } catch (e) {
        console.error('Registration API error:', e?.response?.data || e)
        const raw = e?.response?.data
        const data = (raw && typeof raw === 'object' && raw.errors) ? raw.errors : raw
        let message = e?.message || 'Registration failed'
        if (data) {
          if (typeof data === 'string') {
            message = data
          } else if (typeof data === 'object') {
            const pick = (v) => Array.isArray(v) ? v[0] : (v ?? '')
            // Prefer specific field messages first
            message = pick(data.email) || pick(data.password) || pick(data.confirm_password) || pick(data.first_name) || pick(data.last_name) || pick(data.non_field_errors) || pick(data.role) || (Object.values(data).flat?.()[0] || 'Registration failed')
          }
        }
        this.error = message
        throw new Error(message)
      } finally {
        this.loading = false
      }
    },

    async login({ email, password }) {
      this.loading = true
      this.error = null
      try {
        const { data } = await api.post('/users/login/', { email, password })
        this._saveSession(data.token, data.user)
        return data
      } catch (e) {
        console.error('Login API error:', e?.response?.data || e)
        const message = e?.response?.data?.message || e?.message || 'Login failed'
        this.error = message
        throw new Error(message)
      } finally {
        this.loading = false
      }
    },

    async fetchMe() {
      if (!this.token) { this.loadFromStorage() }
      if (!this.token) return null
      this.loading = true
      this.error = null
      try {
        const { data } = await api.get('/users/me/')
        this.user = data
        localStorage.setItem('auth_user', JSON.stringify(data))
        return data
      } catch (e) {
        const message = e?.response?.data?.message || e?.message || 'Failed to fetch profile'
        this.error = message
        throw new Error(message)
      } finally {
        this.loading = false
      }
    },

    async logout() {
      if (!this.token) { this._clearSession(); return }
      this.loading = true
      this.error = null
      try {
        await api.post('/users/logout/')
      } catch (_) {
        // ignore network errors on logout
      } finally {
        this._clearSession()
        this.loading = false
      }
    },
  },
})
