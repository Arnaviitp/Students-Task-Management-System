<template>
  <div class="task-wrapper">
    <article class="task" :class="[`task--${task.status}`]">
      <div class="status-indicator" :class="[`status--${task.status}`]"></div>
      
      <div class="task__main">
        <div class="row" style="align-items:center">
          <div class="task__title">{{ task.title }}</div>
          <div class="spacer" />
          <span class="muted" style="font-size: 0.75rem; font-weight: 600">#{{ task.id }}</span>
        </div>

        <div class="task__meta">
          <span class="status-pill" :class="[`status-pill--${task.status}`]">
            {{ prettyStatus(task.status) }}
          </span>
          <span class="priority-pill" :class="[`priority-pill--${task.priority}`]">
            {{ task.priority === 1 ? '🔥 High' : task.priority === 2 ? '⚡ Mid' : '🍃 Low' }}
          </span>
          <span v-if="task.due_date" class="pill" style="display: flex; align-items: center; gap: 4px">
            <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
            {{ formatDue(task.due_date) }}
          </span>
        </div>

        <div v-if="task.description" class="task__desc">{{ task.description }}</div>
      </div>

      <div class="task__actions">
        <button class="btn btn--secondary btn--sm" :disabled="busy" @click="cycleStatus" title="Cycle Status">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 4v6h6"></path><path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"></path></svg>
        </button>
        <button class="btn btn--secondary btn--sm" :disabled="busy" @click="editOpen = !editOpen" title="Edit Task">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
        </button>
        <button class="btn btn--danger btn--sm" :disabled="busy" @click="onDelete" title="Delete Task">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>
        </button>
      </div>
    </article>

    <div v-if="editOpen" class="panel edit-panel">
      <div class="grid">
        <div>
          <div class="label">Title</div>
          <input v-model.trim="draftTitle" class="input" />
        </div>
        <div>
          <div class="label">Due Date</div>
          <input v-model="draftDue" class="input" type="datetime-local" />
        </div>
      </div>
      <div class="grid">
        <div>
          <div class="label">Status</div>
          <select v-model="draftStatus" class="select">
            <option value="todo">To Do</option>
            <option value="in_progress">In Progress</option>
            <option value="done">Done</option>
          </select>
        </div>
        <div>
          <div class="label">Priority</div>
          <select v-model.number="draftPriority" class="select">
            <option :value="1">1 (High)</option>
            <option :value="2">2 (Medium)</option>
            <option :value="3">3 (Low)</option>
          </select>
        </div>
      </div>
      <div>
        <div class="label">Description</div>
        <textarea v-model="draftDesc" class="textarea" />
      </div>
      <div class="row" style="margin-top:20px; align-items:center">
        <button class="btn btn--ok" :disabled="busy || !draftTitle" @click="onSave">Update Task</button>
        <button class="btn btn--secondary" @click="editOpen = false">Cancel</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Task, TaskStatus } from "~/types/task";

const props = defineProps<{ task: Task }>();
const emit = defineEmits<{
  (e: "changed"): void;
  (e: "deleted"): void;
}>();

const { update, remove } = useTasks();
const toast = useToast();

const editOpen = ref(false);
const busy = ref(false);

const draftTitle = ref(props.task.title);
const draftDesc = ref<string | null>(props.task.description);
const draftStatus = ref<TaskStatus>(props.task.status);
const draftPriority = ref<1 | 2 | 3>(props.task.priority);
const draftDue = ref<string>(props.task.due_date ? toLocalInput(props.task.due_date) : "");

watch(
  () => props.task,
  (t) => {
    draftTitle.value = t.title;
    draftDesc.value = t.description;
    draftStatus.value = t.status;
    draftPriority.value = t.priority;
    draftDue.value = t.due_date ? toLocalInput(t.due_date) : "";
  }
);

function prettyStatus(s: TaskStatus) {
  if (s === "todo") return "To Do";
  if (s === "in_progress") return "In Progress";
  return "Done";
}

function formatDue(iso: string) {
  const d = new Date(iso);
  return d.toLocaleDateString(undefined, { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
}

function toLocalInput(iso: string) {
  const d = new Date(iso);
  const pad = (n: number) => String(n).padStart(2, "0");
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`;
}

function toIso(value: string) {
  if (!value) return null;
  const d = new Date(value);
  if (Number.isNaN(d.getTime())) return null;
  return d.toISOString();
}

const cycleStatus = async () => {
  const next: TaskStatus =
    props.task.status === "todo" ? "in_progress" : props.task.status === "in_progress" ? "done" : "todo";
  await onPatch({ status: next });
  toast.info(`Status updated to ${prettyStatus(next)}`);
};

const onSave = async () => {
  await onPatch({
    title: draftTitle.value,
    description: draftDesc.value || null,
    status: draftStatus.value,
    priority: draftPriority.value,
    due_date: toIso(draftDue.value),
  });
  editOpen.value = false;
  toast.success("Task updated");
};

const onPatch = async (payload: any) => {
  busy.value = true;
  try {
    await update(props.task.id, payload);
    emit("changed");
  } catch (e: any) {
    const msg = e?.data?.detail || e?.message || "Update failed";
    toast.error(msg);
  } finally {
    busy.value = false;
  }
};

const onDelete = async () => {
  if (!confirm(`Delete task "${props.task.title}"?`)) return;
  busy.value = true;
  try {
    await remove(props.task.id);
    emit("deleted");
  } catch (e: any) {
    const msg = e?.data?.detail || e?.message || "Delete failed";
    toast.error(msg);
  } finally {
    busy.value = false;
  }
};
</script>

<style scoped>
.task-wrapper {
  margin-bottom: 8px;
}

.edit-panel {
  margin-top: 8px;
  background: rgba(255, 255, 255, 0.03);
  border-style: dashed;
}

.btn--sm {
  padding: 8px;
  border-radius: 8px;
}

.status-pill {
  font-size: 0.75rem;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 6px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.status-pill--todo { background: rgba(156, 163, 175, 0.15); color: #9ca3af; }
.status-pill--in_progress { background: rgba(59, 130, 246, 0.15); color: #3b82f6; }
.status-pill--done { background: rgba(16, 185, 129, 0.15); color: #10b981; }

.priority-pill {
  font-size: 0.75rem;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 6px;
}

.priority-pill--1 { color: #fb7185; background: rgba(251, 113, 133, 0.1); }
.priority-pill--2 { color: #facc15; background: rgba(250, 204, 21, 0.1); }
.priority-pill--3 { color: #34d399; background: rgba(52, 211, 153, 0.1); }

.task--done {
  opacity: 0.8;
}

.task--done .task__title {
  text-decoration: line-through;
  color: var(--muted);
}
</style>

