<template>
  <section class="hero">
    <img
      v-if="heroImage"
      :src="heroImage"
      :alt="name"
      class="hero-image"
    />
    <div class="hero-content">
      <h1>{{ name }}</h1>
      <p v-if="tagline">{{ tagline }}</p>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useSettingsStore } from '@/stores/settings'

const { data } = storeToRefs(useSettingsStore())
const name = computed(() => data.value?.photographer_name || '')
const tagline = computed(() => data.value?.tagline || '')
const heroImage = computed(() => data.value?.hero_image_url || null)
</script>

<style scoped>
.hero {
  position: relative;
  height: 90vh;
  min-height: 500px;
  overflow: hidden;
  background: #2c2c2a;
}
.hero-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.hero-content {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: #ffffff;
  text-shadow: 0 2px 20px rgba(0, 0, 0, 0.5);
  padding: 0 20px;
  text-align: center;
}
h1 {
  font-size: clamp(32px, 6vw, 72px);
  font-weight: 300;
  letter-spacing: 0.05em;
}
p {
  font-size: clamp(14px, 1.5vw, 20px);
  opacity: 0.9;
  margin-top: 12px;
}
</style>
