<template>
  <section class="panel">
    <div class="row" style="align-items:center">
      <div style="font-weight:700; font-family: var(--font-title); font-size: 1.1rem">Create New Task</div>
      <div class="spacer" />
      <span class="pill">Save to Cloud</span>
    </div>

    <div class="grid" style="margin-top:20px">
      <div>
        <div class="label">Task Title</div>
        <input v-model.trim="title" class="input" placeholder="e.g. Finish math assignment" @keydown.enter="onCreate" />
      </div>
      <div>
        <div class="label">Due Date</div>
        <input v-model="dueDate" class="input" type="datetime-local" />
      </div>
    </div>

    <div class="grid">
      <div>
        <div class="label">Current Status</div>
        <select v-model="status" class="select">
          <option value="todo">To Do</option>
          <option value="in_progress">In Progress</option>
          <option value="done">Done</option>
        </select>
      </div>
      <div>
        <div class="label">Priority Level</div>
        <select v-model.number="priority" class="select">
          <option :value="1">🔥 High Priority</option>
          <option :value="2">⚡ Medium Priority</option>
          <option :value="3">🍃 Low Priority</option>
        </select>
      </div>
    </div>

    <div>
      <div class="label">Description & Notes</div>
      <textarea v-model="description" class="textarea" placeholder="Add some details about this task..." />
    </div>

    <div class="row" style="margin-top:24px; align-items:center">
      <button class="btn" :disabled="busy || !title" @click="onCreate">
        <span v-if="busy">Creating...</span>
        <template v-else>
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
          Add Task
        </template>
      </button>
      <div class="spacer" />
      <span class="muted" style="font-size:0.8125rem">Automatically syncs with backend</span>
    </div>
  </section>
</template>

<script setup lang="ts">
import type { TaskCreate, TaskStatus } from "~/types/task";

const emit = defineEmits<{
  (e: "created"): void;
}>();

const { create } = useTasks();
const toast = useToast();

const title = ref("");
const description = ref<string | null>(null);
const status = ref<TaskStatus>("todo");
const priority = ref<1 | 2 | 3>(2);
const dueDate = ref<string>("");

const busy = ref(false);

const toIso = (value: string) => {
  if (!value) return null;
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return null;
  return date.toISOString();
};

const onCreate = async () => {
  if (!title.value) return;
  busy.value = true;
  try {
    const payload: TaskCreate = {
      title: title.value,
      description: description.value || null,
      status: status.value,
      priority: priority.value,
      due_date: toIso(dueDate.value),
    };
    await create(payload);
    title.value = "";
    description.value = null;
    status.value = "todo";
    priority.value = 2;
    dueDate.value = "";
    toast.success("Task created successfully!");
    emit("created");
  } catch (e: any) {
    const msg = e?.data?.detail || e?.message || "Failed to create task";
    toast.error(msg);
  } finally {
    busy.value = false;
  }
};
</script>

