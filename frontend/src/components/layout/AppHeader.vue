<template>
  <header class="header">
    <router-link to="/" class="brand">{{ brandName }}</router-link>
    <nav class="nav">
      <router-link to="/">{{ $t('nav.home') }}</router-link>
      <router-link to="/portfolio">{{ $t('nav.portfolio') }}</router-link>
      <LangSwitcher />
    </nav>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useSettingsStore } from '@/stores/settings'
import LangSwitcher from './LangSwitcher.vue'

const { data } = storeToRefs(useSettingsStore())
const brandName = computed(() => data.value?.photographer_name || 'Portfolio')
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 32px;
  position: sticky;
  top: 0;
  background: color-mix(in srgb, var(--color-bg) 85%, transparent);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  z-index: 10;
  border-bottom: 1px solid color-mix(in srgb, var(--color-text) 8%, transparent);
}
.brand {
  font-weight: 500;
  letter-spacing: 0.02em;
  font-size: 15px;
}
.nav {
  display: flex;
  gap: 28px;
  align-items: center;
  font-size: 14px;
}
.nav a {
  opacity: 0.6;
  transition: opacity 0.2s;
}
.nav a:hover,
.nav a.router-link-exact-active {
  opacity: 1;
}
@media (max-width: 640px) {
  .header { padding: 16px 20px; }
  .nav { gap: 18px; }
}
</style>
