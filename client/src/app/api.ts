import axios from 'axios'
import { API_BASE } from '../shared/config'

export const api = axios.create({ baseURL: API_BASE })

export async function login(vk_user_id: string, username?: string) {
  const res = await api.post('/api/v1/auth/login', { vk_user_id, username })
  return res.data as { access_token: string }
}

export async function getInventory(token: string) {
  const res = await api.get('/api/v1/profile/inventory', {
    headers: { Authorization: `Bearer ${token}` }
  })
  return res.data as Array<{ id: string; name: string; rarity: string }>
}