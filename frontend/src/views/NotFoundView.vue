<template>
  <section class="not-found">
    <h1>404</h1>
    <p>{{ $t('not_found.title') }}</p>
    <router-link to="/">{{ $t('not_found.back') }}</router-link>
  </section>
</template>

<style scoped>
.not-found {
  text-align: center;
  padding: 120px 24px;
}
h1 {
  font-size: 72px;
  font-weight: 300;
  color: var(--color-muted);
}
p {
  font-size: 18px;
  margin-bottom: 24px;
}
a {
  color: var(--color-accent);
  border-bottom: 1px solid;
}
</style>
