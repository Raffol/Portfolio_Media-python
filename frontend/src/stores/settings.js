import { defineStore } from 'pinia'
import client from '@/api/client'

export const useSettingsStore = defineStore('settings', {
  state: () => ({
    data: null,
    loaded: false,
  }),
  actions: {
    async load() {
      if (this.loaded) return
      try {
        this.data = await client.get('/settings/').then((r) => r.data)
        this.applyPalette()
        this.loaded = true
      } catch (e) {
        console.error('Не удалось загрузить настройки сайта:', e)
      }
    },
    applyPalette() {
      if (!this.data) return
      const root = document.documentElement
      const { color_bg, color_text, color_muted, color_accent } = this.data
      if (color_bg) root.style.setProperty('--color-bg', color_bg)
      if (color_text) root.style.setProperty('--color-text', color_text)
      if (color_muted) root.style.setProperty('--color-muted', color_muted)
      if (color_accent) root.style.setProperty('--color-accent', color_accent)
    },
  },
})
