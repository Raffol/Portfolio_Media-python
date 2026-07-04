import axios from 'axios'
import i18n from '@/i18n'

const client = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
})

client.interceptors.request.use((config) => {
  config.headers['Accept-Language'] = i18n.global.locale.value
  return config
})

export default client
