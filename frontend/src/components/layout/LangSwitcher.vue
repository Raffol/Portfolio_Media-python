<template>
  <div class="lang">
    <button
      v-for="lang in langs"
      :key="lang"
      :class="{ active: locale === lang }"
      @click="switchTo(lang)"
    >
      {{ lang.toUpperCase() }}
    </button>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import { useSettingsStore } from '@/stores/settings'

const { locale } = useI18n()
const settingsStore = useSettingsStore()
const langs = ['ru', 'en']

async function switchTo(lang) {
  locale.value = lang
  localStorage.setItem('locale', lang)
  // Перезагружаем настройки на новом языке
  settingsStore.loaded = false
  await settingsStore.load()
}
</script>

<style scoped>
.lang {
  display: flex;
  gap: 6px;
  padding-left: 16px;
  border-left: 1px solid color-mix(in srgb, var(--color-text) 12%, transparent);
}
.lang button {
  font-size: 12px;
  opacity: 0.4;
  padding: 4px 2px;
  font-family: inherit;
  color: inherit;
  transition: opacity 0.2s;
}
.lang button.active {
  opacity: 1;
  font-weight: 500;
}
</style>
