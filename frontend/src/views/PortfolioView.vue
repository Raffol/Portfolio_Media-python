<template>
  <section class="portfolio">
    <div v-if="loading" class="loader">{{ $t('portfolio.loading') }}</div>
    <div v-else-if="!works.length" class="loader">{{ $t('portfolio.empty') }}</div>
    <div v-else class="grid">
      <WorkCard v-for="work in works" :key="work.slug" :work="work" />
    </div>
  </section>
</template>

<script setup>
import { useWorks } from '@/composables/useWorks'
import WorkCard from '@/components/WorkCard.vue'

const { works, loading } = useWorks()
</script>

<style scoped>
.portfolio {
  padding: 48px 32px;
  max-width: 1600px;
  margin: 0 auto;
}
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 24px;
}
.loader {
  text-align: center;
  padding: 120px 0;
  color: var(--color-muted);
}
@media (max-width: 640px) {
  .portfolio { padding: 32px 20px; }
  .grid { grid-template-columns: 1fr; gap: 20px; }
}
</style>
