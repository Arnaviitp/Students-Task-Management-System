<template>
  <section class="panel">
    <div class="row" style="align-items:center">
      <div style="font-weight:700; font-family: var(--font-title); font-size: 1.1rem">My Tasks</div>
      <div class="spacer" />
      <span class="pill">{{ tasks.length }} Tasks</span>
    </div>

    <div class="grid" style="margin-top:20px">
      <div style="position: relative">
        <div class="label">Search Tasks</div>
        <div style="position: relative">
          <input v-model.trim="q" class="input" style="padding-left: 40px" placeholder="title or description" @keydown.enter="refresh" />
          <svg style="position: absolute; left: 14px; top: 50%; transform: translateY(-50%); color: var(--muted)" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        </div>
      </div>
      <div>
        <div class="label">Filter Status</div>
        <select v-model="status" class="select" @change="refresh">
          <option value="">All Tasks</option>
          <option value="todo">To Do</option>
          <option value="in_progress">In Progress</option>
          <option value="done">Done</option>
        </select>
      </div>
    </div>

    <div class="row" style="margin-top:20px; align-items:center">
      <button class="btn btn--secondary" :disabled="busy" @click="refresh">
        <svg :class="{ 'spin': busy }" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M23 4v6h-6"></path><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"></path></svg>
        Refresh
      </button>
      <div class="spacer" />
      <span v-if="busy" class="muted" style="font-size:0.8125rem">Syncing data...</span>
    </div>

    <div style="margin-top:24px; display:flex; flex-direction:column; gap:12px">
      <TransitionGroup name="list">
        <TaskItem
          v-for="t in tasks"
          :key="t.id"
          :task="t"
          @changed="refresh"
          @deleted="handleDelete"
        />
      </TransitionGroup>
      <div v-if="!busy && tasks.length === 0" class="panel muted" style="text-align: center; background: rgba(0,0,0,0.1); border-style: dashed">
        No tasks found. Start by adding one!
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import type { Task, TaskStatus } from "~/types/task";

const { list } = useTasks();
const toast = useToast();

const q = ref("");
const status = ref<TaskStatus | "">("");
const busy = ref(false);
const tasks = ref<Task[]>([]);

const emit = defineEmits<{
  (e: "loaded", tasks: Task[]): void;
}>();

const refresh = async () => {
  busy.value = true;
  try {
    tasks.value = await list({ q: q.value || undefined, status: status.value, limit: 200 });
    emit("loaded", tasks.value);
  } catch (e: any) {
    const msg = e?.data?.detail || e?.message || "Failed to load tasks";
    toast.error(msg);
  } finally {
    busy.value = false;
  }
};

const handleDelete = () => {
  toast.success("Task deleted");
  refresh();
};

onMounted(refresh);
defineExpose({ refresh, tasks });
</script>

<style scoped>
.spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.list-enter-active, .list-leave-active {
  transition: all 0.4s ease;
}
.list-enter-from, .list-leave-to {
  opacity: 0;
  transform: translateY(20px);
}
</style>

