<template>
  <section class="contact-form">
    <h2>{{ $t('contact.form_title') }}</h2>
    <p class="hint">{{ $t('contact.form_hint') }}</p>

    <form @submit.prevent="submit" novalidate>
      <div class="field">
        <label for="name">{{ $t('contact.field_name') }}</label>
        <input id="name" v-model="form.name" type="text" required :disabled="loading" />
      </div>

      <div class="field">
        <label for="contact">{{ $t('contact.field_contact') }}</label>
        <input
          id="contact"
          v-model="form.contact"
          type="text"
          required
          :disabled="loading"
          :placeholder="$t('contact.field_contact_placeholder')"
        />
      </div>

      <div class="field">
        <label for="message">{{ $t('contact.field_message') }}</label>
        <textarea
          id="message"
          v-model="form.message"
          rows="4"
          :disabled="loading"
          :placeholder="$t('contact.field_message_placeholder')"
        ></textarea>
      </div>

      <input
        v-model="form.website"
        type="text"
        name="website"
        tabindex="-1"
        autocomplete="off"
        class="honeypot"
        aria-hidden="true"
      />

      <button type="submit" :disabled="loading || !isValid">
        {{ loading ? $t('contact.submitting') : $t('contact.submit') }}
      </button>

      <p v-if="status === 'success'" class="msg success">
        {{ $t('contact.success') }}
      </p>
      <p v-if="status === 'error'" class="msg error">
        {{ $t('contact.error') }}
      </p>
    </form>
  </section>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import client from '@/api/client'

const route = useRoute()
const form = ref({ name: '', contact: '', message: '', website: '' })
const loading = ref(false)
const status = ref(null)

const isValid = computed(
  () =>
    form.value.name.trim().length > 1 &&
    form.value.contact.trim().length > 3
)

async function submit() {
  if (!isValid.value || loading.value) return
  loading.value = true
  status.value = null

  try {
    await client.post('/contact/', {
      name: form.value.name.trim(),
      contact: form.value.contact.trim(),
      message: form.value.message.trim(),
      website: form.value.website,
      source_page: route.fullPath,
    })
    status.value = 'success'
    form.value = { name: '', contact: '', message: '', website: '' }
  } catch (e) {
    status.value = 'error'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.contact-form {
  max-width: 520px;
  margin: 0 auto;
  padding: 40px 24px 80px;
}
h2 {
  font-size: 24px;
  font-weight: 300;
  text-align: center;
  margin-bottom: 8px;
}
.hint {
  text-align: center;
  color: var(--color-muted);
  font-size: 14px;
  margin-bottom: 32px;
}
.field { margin-bottom: 20px; }
label {
  display: block;
  font-size: 13px;
  color: var(--color-muted);
  margin-bottom: 6px;
}
input[type='text'],
textarea {
  width: 100%;
  padding: 12px 14px;
  border: 1px solid color-mix(in srgb, var(--color-text) 15%, transparent);
  border-radius: 4px;
  background: transparent;
  color: var(--color-text);
  font-size: 15px;
  font-family: inherit;
  transition: border-color 0.2s;
}
input:focus,
textarea:focus {
  outline: none;
  border-color: var(--color-accent);
}
textarea { resize: vertical; min-height: 100px; }
button {
  width: 100%;
  padding: 14px;
  background: var(--color-accent);
  color: var(--color-bg);
  border-radius: 4px;
  font-size: 15px;
  font-weight: 500;
  transition: opacity 0.2s;
}
button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.msg {
  margin-top: 20px;
  padding: 12px;
  border-radius: 4px;
  text-align: center;
  font-size: 14px;
}
.msg.success { background: #e8f5e8; color: #2d5a2d; }
.msg.error { background: #fbe8e8; color: #8a2a2a; }
.honeypot {
  position: absolute !important;
  left: -9999px !important;
  width: 1px !important;
  height: 1px !important;
  opacity: 0 !important;
  pointer-events: none !important;
}
</style>
