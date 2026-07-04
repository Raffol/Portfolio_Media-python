import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import i18n from './i18n'
import { useSettingsStore } from './stores/settings'

import './assets/styles/reset.css'
import './assets/styles/main.css'

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(i18n)

// Загружаем настройки до монтирования, чтобы палитра применилась сразу
useSettingsStore().load().finally(() => {
  app.mount('#app')
})
