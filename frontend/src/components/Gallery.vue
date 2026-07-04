<template>
  <div class="gallery" ref="galleryEl" @contextmenu.prevent>
    <a
      v-for="photo in photos"
      :key="photo.id"
      :href="photo.full_url"
      :data-pswp-width="photo.width"
      :data-pswp-height="photo.height"
      class="gallery-item"
      target="_blank"
      rel="noopener"
    >
      <img :src="photo.preview_url" alt="" loading="lazy" />
    </a>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import PhotoSwipeLightbox from 'photoswipe/lightbox'
import 'photoswipe/style.css'

const props = defineProps({
  photos: { type: Array, default: () => [] },
})

const galleryEl = ref(null)
let lightbox = null

function initLightbox() {
  if (lightbox) {
    lightbox.destroy()
    lightbox = null
  }
  if (!galleryEl.value || !props.photos.length) return
  lightbox = new PhotoSwipeLightbox({
    gallery: galleryEl.value,
    children: 'a',
    pswpModule: () => import('photoswipe'),
  })
  lightbox.init()
}

onMounted(() => {
  nextTick(initLightbox)
})

watch(
  () => props.photos,
  () => nextTick(initLightbox),
  { deep: true }
)

onUnmounted(() => {
  lightbox?.destroy()
  lightbox = null
})
</script>

<style scoped>
.gallery {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 8px;
}
.gallery-item {
  display: block;
  aspect-ratio: 3 / 2;
  overflow: hidden;
  background: color-mix(in srgb, var(--color-text) 6%, transparent);
}
.gallery-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  user-select: none;
  -webkit-user-drag: none;
  pointer-events: none;
}
</style>
