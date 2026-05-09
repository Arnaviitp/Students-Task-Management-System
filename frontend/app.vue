<template>
  <div class="app">
    <header class="header">
      <div class="container header__inner">
        <div class="brand">
          <div class="brand__title">Student Task Manager</div>
          <div class="brand__subtitle">Create, track, and finish your tasks</div>
        </div>
        <a class="link" :href="`${apiBase}/docs`" target="_blank" rel="noreferrer">API Docs</a>
      </div>
    </header>
    <main class="container main">
      <NuxtPage />
    </main>
    <footer class="footer">
      <div class="container footer__inner">
        <span>Backend: {{ apiBase }}</span>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
const config = useRuntimeConfig();
const apiBase = computed(() => config.public.apiBase as string);
</script>

