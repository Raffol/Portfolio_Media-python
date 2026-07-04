<template>
  <footer class="footer">
    <div class="content">
      <span class="brand">{{ brandName }}</span>
      <span class="rights">© {{ year }} · {{ $t('footer.rights') }}</span>
    </div>
  </footer>
</template>

<script setup>
import { computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useSettingsStore } from '@/stores/settings'

const { data } = storeToRefs(useSettingsStore())
const brandName = computed(() => data.value?.photographer_name || 'Portfolio')
const year = new Date().getFullYear()
</script>

<style scoped>
.footer {
  padding: 40px 32px;
  border-top: 1px solid color-mix(in srgb, var(--color-text) 8%, transparent);
  margin-top: 80px;
}
.content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  font-size: 13px;
  color: var(--color-muted);
}
.brand { font-weight: 500; color: var(--color-text); }
@media (max-width: 640px) {
  .content { flex-direction: column; gap: 8px; }
}
</style>
