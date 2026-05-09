<template>
  <div class="app">
    <header class="header">
      <div class="container header__inner">
        <div class="brand">
          <div class="brand__title">Arnav's Task Manager</div>
          <div class="brand__subtitle">Stay organized, stay productive</div>
        </div>
        <nav class="nav">
          <a class="link" :href="`${apiBase}/docs`" target="_blank" rel="noreferrer">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
            API Docs
          </a>
        </nav>
      </div>
    </header>

    <main class="container main">
      <NuxtPage />
    </main>

    <footer class="footer">
      <div class="container footer__inner row" style="align-items: center">
        <span>&copy; 2026 Student Task Manager</span>
        <div class="spacer"></div>
        <span class="pill">Backend: {{ apiBase }}</span>
      </div>
    </footer>

    <!-- Toast Notifications -->
    <div class="toast-container">
      <TransitionGroup name="toast">
        <div v-for="toast in toasts" :key="toast.id" :class="['toast', `toast--${toast.type}`]" @click="remove(toast.id)">
          {{ toast.message }}
        </div>
      </TransitionGroup>
    </div>
  </div>
</template>

<script setup lang="ts">
const config = useRuntimeConfig();
const apiBase = computed(() => config.public.apiBase as string);
const { toasts, remove } = useToast();

useHead({
  title: 'Task Manager | Modern Productivity',
  meta: [
    { name: 'description', content: 'A premium, modern task management system for students. Create, track, and finish your tasks with ease.' },
    { property: 'og:title', content: 'Task Manager | Modern Productivity' },
    { property: 'og:description', content: 'A premium, modern task management system for students.' },
    { name: 'theme-color', content: '#030712' }
  ],
  link: [
    { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
  ]
});
</script>

<style scoped>
.app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main {
  flex: 1;
}

.nav {
  display: flex;
  gap: 20px;
}

.link {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.9375rem;
}

.toast-container {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.toast {
  padding: 12px 20px;
  border-radius: var(--radius-md);
  background: var(--panel);
  border: 1px solid var(--border);
  color: var(--text);
  font-size: 0.875rem;
  font-weight: 500;
  box-shadow: var(--shadow-lg);
  cursor: pointer;
  min-width: 200px;
  backdrop-filter: blur(8px);
}

.toast--success { border-left: 4px solid var(--ok); }
.toast--error { border-left: 4px solid var(--danger); }
.toast--info { border-left: 4px solid var(--accent); }

.toast-enter-active, .toast-leave-active {
  transition: all 0.3s ease;
}
.toast-enter-from {
  opacity: 0;
  transform: translateX(30px);
}
.toast-leave-to {
  opacity: 0;
  transform: scale(0.9);
}
</style>

