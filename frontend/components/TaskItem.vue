<template>
  <article class="task">
    <div class="task__main">
      <div class="row" style="align-items:center">
        <div class="task__title">{{ task.title }}</div>
        <div class="spacer" />
        <span class="pill">#{{ task.id }}</span>
      </div>

      <div class="task__meta">
        <span class="pill">Status: {{ prettyStatus(task.status) }}</span>
        <span class="pill">Priority: {{ task.priority }}</span>
        <span v-if="task.due_date" class="pill">Due: {{ formatDue(task.due_date) }}</span>
      </div>

      <div v-if="task.description" class="task__desc">{{ task.description }}</div>
    </div>

    <div class="task__actions">
      <button class="btn" :disabled="busy" @click="cycleStatus">Next status</button>
      <button class="btn" :disabled="busy" @click="editOpen = !editOpen">{{ editOpen ? "Close" : "Edit" }}</button>
      <button class="btn btn--danger" :disabled="busy" @click="onDelete">Delete</button>
    </div>
  </article>

  <div v-if="editOpen" class="panel" style="margin-top:10px">
    <div class="grid">
      <div>
        <div class="label">Title</div>
        <input v-model.trim="draftTitle" class="input" />
      </div>
      <div>
        <div class="label">Due date</div>
        <input v-model="draftDue" class="input" type="datetime-local" />
      </div>
    </div>
    <div class="grid">
      <div>
        <div class="label">Status</div>
        <select v-model="draftStatus" class="select">
          <option value="todo">To do</option>
          <option value="in_progress">In progress</option>
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
    <div class="row" style="margin-top:12px; align-items:center">
      <button class="btn btn--ok" :disabled="busy || !draftTitle" @click="onSave">Save</button>
      <span v-if="error" class="error">{{ error }}</span>
      <div class="spacer" />
      <span class="muted" style="font-size:12px">Edits update the backend task.</span>
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

const editOpen = ref(false);
const busy = ref(false);
const error = ref<string | null>(null);

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
  if (s === "todo") return "To do";
  if (s === "in_progress") return "In progress";
  return "Done";
}

function formatDue(iso: string) {
  const d = new Date(iso);
  return d.toLocaleString();
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
};

const onPatch = async (payload: any) => {
  error.value = null;
  busy.value = true;
  try {
    await update(props.task.id, payload);
    emit("changed");
  } catch (e: any) {
    error.value = e?.data?.detail || e?.message || "Update failed";
  } finally {
    busy.value = false;
  }
};

const onDelete = async () => {
  if (!confirm(`Delete task #${props.task.id}?`)) return;
  error.value = null;
  busy.value = true;
  try {
    await remove(props.task.id);
    emit("deleted");
  } catch (e: any) {
    error.value = e?.data?.detail || e?.message || "Delete failed";
  } finally {
    busy.value = false;
  }
};
</script>

