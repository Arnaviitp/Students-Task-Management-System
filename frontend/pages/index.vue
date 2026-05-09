<template>
  <div style="display:flex; flex-direction:column; gap:14px">
    <TaskForm @created="refreshAll" />
    <TaskList ref="taskListRef" />
  </div>
</template>

<script setup lang="ts">
const taskListRef = ref<{ refresh: () => Promise<void> } | null>(null);

const refreshAll = async () => {
  await taskListRef.value?.refresh();
};
</script>

