<template>
  <div class="dashboard">
    <div class="welcome-section">
      <h1 class="welcome-title">Dashboard</h1>
      <p class="welcome-text">You have <span class="highlight">{{ todoCount }}</span> tasks remaining for today.</p>
    </div>

    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-label">Total Tasks</div>
        <div class="stat-value">{{ tasks.length }}</div>
      </div>
      <div class="stat-card stat-card--active">
        <div class="stat-label">In Progress</div>
        <div class="stat-value">{{ progressCount }}</div>
      </div>
      <div class="stat-card stat-card--done">
        <div class="stat-label">Completed</div>
        <div class="stat-value">{{ doneCount }}</div>
      </div>
    </div>

    <div class="content-grid">
      <TaskForm @created="refreshAll" />
      <TaskList ref="taskListRef" @loaded="updateStats" />
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Task } from "~/types/task";

const taskListRef = ref<{ refresh: () => Promise<void>, tasks: Task[] } | null>(null);
const tasks = ref<Task[]>([]);

const todoCount = computed(() => tasks.value.filter(t => t.status === 'todo').length);
const progressCount = computed(() => tasks.value.filter(t => t.status === 'in_progress').length);
const doneCount = computed(() => tasks.value.filter(t => t.status === 'done').length);

const refreshAll = async () => {
  await taskListRef.value?.refresh();
};

const updateStats = (newTasks: Task[]) => {
  tasks.value = newTasks;
};
</script>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.welcome-section {
  margin-bottom: 8px;
}

.welcome-title {
  font-family: var(--font-title);
  font-size: 2rem;
  font-weight: 700;
  margin: 0;
  letter-spacing: -0.02em;
}

.welcome-text {
  color: var(--muted);
  margin-top: 8px;
  font-size: 1.1rem;
}

.highlight {
  color: var(--accent);
  font-weight: 600;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.stat-card {
  background: var(--glass);
  border: 1px solid var(--border);
  padding: 24px;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
}

.stat-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.stat-value {
  font-size: 2.25rem;
  font-weight: 700;
  font-family: var(--font-title);
  margin-top: 8px;
}

.stat-card--active .stat-value { color: var(--accent); }
.stat-card--done .stat-value { color: var(--ok); }

.content-grid {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

@media (min-width: 1024px) {
  .content-grid {
    display: grid;
    grid-template-columns: 400px 1fr;
    align-items: start;
  }
}
</style>

