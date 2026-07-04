<template>
  <article v-if="work" class="work">
    <router-link to="/portfolio" class="back">{{ $t('work.back') }}</router-link>
    <header class="work-header">
      <h1>{{ work.title }}</h1>
      <p v-if="work.description" class="description">{{ work.description }}</p>
    </header>
    <Gallery :photos="work.photos" />
  </article>
  <div v-else-if="loading" class="loader">{{ $t('portfolio.loading') }}</div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { getWork } from '@/api/works'
import Gallery from '@/components/Gallery.vue'

const props = defineProps({ slug: String })
const work = ref(null)
const loading = ref(true)

async function load() {
  loading.value = true
  try {
    work.value = await getWork(props.slug)
  } catch (e) {
    console.error(e)
    work.value = null
  } finally {
    loading.value = false
  }
}

watch(() => props.slug, load, { immediate: true })
</script>

<style scoped>
.work {
  max-width: 1600px;
  margin: 0 auto;
  padding: 32px;
}
.back {
  display: inline-block;
  font-size: 13px;
  color: var(--color-muted);
  margin-bottom: 24px;
  transition: color 0.2s;
}
.back:hover { color: var(--color-text); }

.work-header {
  text-align: center;
  margin-bottom: 48px;
}
h1 {
  font-size: clamp(28px, 4vw, 44px);
  font-weight: 300;
  margin-bottom: 16px;
}
.description {
  color: var(--color-muted);
  max-width: 600px;
  margin: 0 auto;
}
.loader {
  text-align: center;
  padding: 120px 0;
  color: var(--color-muted);
}
</style>
