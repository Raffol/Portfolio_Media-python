<template>
  <router-link :to="`/portfolio/${work.slug}`" class="card">
    <div class="cover">
      <img v-if="work.cover_url" :src="work.cover_url" :alt="work.title" loading="lazy" />
      <div v-else class="cover-placeholder"></div>
    </div>
    <h3>{{ work.title }}</h3>
  </router-link>
</template>

<script setup>
defineProps({
  work: { type: Object, required: true },
})
</script>

<style scoped>
.card {
  display: block;
  transition: transform 0.3s ease;
}
.card:hover { transform: translateY(-4px); }

.cover {
  aspect-ratio: 3 / 2;
  overflow: hidden;
  background: color-mix(in srgb, var(--color-text) 6%, transparent);
  margin-bottom: 12px;
  border-radius: 2px;
}
.cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.6s ease;
}
.card:hover .cover img { transform: scale(1.03); }
.cover-placeholder {
  width: 100%;
  height: 100%;
  background: color-mix(in srgb, var(--color-text) 8%, transparent);
}
h3 {
  font-size: 15px;
  font-weight: 400;
  margin: 0;
}
</style>
