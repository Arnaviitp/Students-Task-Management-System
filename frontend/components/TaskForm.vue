<template>
  <section class="panel">
    <div class="row" style="align-items:center">
      <div style="font-weight:750">New task</div>
      <div class="spacer" />
      <span class="pill">Priority: 1 high · 3 low</span>
    </div>

    <div class="grid" style="margin-top:12px">
      <div>
        <div class="label">Title</div>
        <input v-model.trim="title" class="input" placeholder="e.g. Finish math assignment" />
      </div>
      <div>
        <div class="label">Due date (optional)</div>
        <input v-model="dueDate" class="input" type="datetime-local" />
      </div>
    </div>

    <div class="grid">
      <div>
        <div class="label">Status</div>
        <select v-model="status" class="select">
          <option value="todo">To do</option>
          <option value="in_progress">In progress</option>
          <option value="done">Done</option>
        </select>
      </div>
      <div>
        <div class="label">Priority</div>
        <select v-model.number="priority" class="select">
          <option :value="1">1 (High)</option>
          <option :value="2">2 (Medium)</option>
          <option :value="3">3 (Low)</option>
        </select>
      </div>
    </div>

    <div>
      <div class="label">Description (optional)</div>
      <textarea v-model="description" class="textarea" placeholder="Notes, subtasks, links..." />
    </div>

    <div class="row" style="margin-top:12px; align-items:center">
      <button class="btn btn--ok" :disabled="busy || !title" @click="onCreate">Add task</button>
      <span v-if="error" class="error">{{ error }}</span>
      <div class="spacer" />
      <span class="muted" style="font-size:12px">Tasks are saved to your local backend DB.</span>
    </div>
  </section>
</template>

<script setup lang="ts">
import type { TaskCreate, TaskStatus } from "~/types/task";

const emit = defineEmits<{
  (e: "created"): void;
}>();

const { create } = useTasks();

const title = ref("");
const description = ref<string | null>(null);
const status = ref<TaskStatus>("todo");
const priority = ref<1 | 2 | 3>(2);
const dueDate = ref<string>("");

const busy = ref(false);
const error = ref<string | null>(null);

const toIso = (value: string) => {
  if (!value) return null;
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return null;
  return date.toISOString();
};

const onCreate = async () => {
  error.value = null;
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
    emit("created");
  } catch (e: any) {
    error.value = e?.data?.detail || e?.message || "Failed to create task";
  } finally {
    busy.value = false;
  }
};
</script>

