<template>
  <section class="contact">
    <p class="lead" v-if="heading">{{ heading }}</p>
    <a v-if="phone" class="phone" :href="`tel:${cleanPhone}`">{{ phone }}</a>
    <div class="socials">
      <a v-if="data?.vk_url" :href="data.vk_url" target="_blank" rel="noopener">ВКонтакте</a>
      <a v-if="data?.instagram_url" :href="data.instagram_url" target="_blank" rel="noopener">Instagram</a>
      <a v-if="data?.telegram_url" :href="data.telegram_url" target="_blank" rel="noopener">Telegram</a>
      <a v-if="data?.youtube_url" :href="data.youtube_url" target="_blank" rel="noopener">YouTube</a>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useSettingsStore } from '@/stores/settings'

const { data } = storeToRefs(useSettingsStore())
const heading = computed(() => data.value?.contact_heading || '')
const phone = computed(() => data.value?.phone || '')
const cleanPhone = computed(() => phone.value.replace(/[\s()-]/g, ''))
</script>

<style scoped>
.contact {
  padding: 100px 24px 40px;
  text-align: center;
  max-width: 720px;
  margin: 0 auto;
}
.lead {
  font-size: 17px;
  color: var(--color-muted);
  margin-bottom: 28px;
}
.phone {
  display: inline-block;
  font-size: clamp(26px, 4vw, 40px);
  font-weight: 300;
  margin-bottom: 40px;
  color: var(--color-text);
}
.socials {
  display: flex;
  justify-content: center;
  gap: 28px;
  flex-wrap: wrap;
  font-size: 14px;
}
.socials a {
  color: var(--color-muted);
  transition: color 0.2s;
}
.socials a:hover {
  color: var(--color-accent);
}
</style>
