import { createI18n } from 'vue-i18n'
import ru from './ru.json'
import en from './en.json'

const savedLocale = localStorage.getItem('locale') || 'ru'

export default createI18n({
  legacy: false,
  locale: savedLocale,
  fallbackLocale: 'ru',
  messages: { ru, en },
})
