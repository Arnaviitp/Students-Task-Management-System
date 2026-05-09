<template>
  <section class="panel">
    <div class="row" style="align-items:center">
      <div style="font-weight:750">Tasks</div>
      <div class="spacer" />
      <span class="pill">{{ tasks.length }} shown</span>
    </div>

    <div class="grid" style="margin-top:12px">
      <div>
        <div class="label">Search</div>
        <input v-model.trim="q" class="input" placeholder="title or description" @keydown.enter="refresh" />
      </div>
      <div>
        <div class="label">Status</div>
        <select v-model="status" class="select" @change="refresh">
          <option value="">All</option>
          <option value="todo">To do</option>
          <option value="in_progress">In progress</option>
          <option value="done">Done</option>
        </select>
      </div>
    </div>

    <div class="row" style="margin-top:12px; align-items:center">
      <button class="btn" :disabled="busy" @click="refresh">Refresh</button>
      <span v-if="error" class="error">{{ error }}</span>
      <div class="spacer" />
      <span v-if="busy" class="muted" style="font-size:12px">Loading…</span>
    </div>

    <div style="margin-top:14px; display:flex; flex-direction:column; gap:10px">
      <TaskItem
        v-for="t in tasks"
        :key="t.id"
        :task="t"
        @changed="refresh"
        @deleted="refresh"
      />
      <div v-if="!busy && tasks.length === 0" class="muted">No tasks yet.</div>
    </div>
  </section>
</template>

<script setup lang="ts">
import type { Task, TaskStatus } from "~/types/task";

const { list } = useTasks();

const q = ref("");
const status = ref<TaskStatus | "">("");
const busy = ref(false);
const error = ref<string | null>(null);
const tasks = ref<Task[]>([]);

const refresh = async () => {
  error.value = null;
  busy.value = true;
  try {
    tasks.value = await list({ q: q.value || undefined, status: status.value, limit: 200 });
  } catch (e: any) {
    error.value = e?.data?.detail || e?.message || "Failed to load tasks";
  } finally {
    busy.value = false;
  }
};

onMounted(refresh);
defineExpose({ refresh });
</script>

