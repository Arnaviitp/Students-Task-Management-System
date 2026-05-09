import type { Task, TaskCreate, TaskStatus, TaskUpdate } from "~/types/task";

export function useTasks() {
  const { request } = useApi();

  const list = async (params: { q?: string; status?: TaskStatus | ""; limit?: number } = {}) => {
    const query: Record<string, any> = {};
    if (params.q) query.q = params.q;
    if (params.status) query.status = params.status;
    if (params.limit) query.limit = params.limit;
    return await request<Task[]>("/tasks", { query });
  };

  const create = async (payload: TaskCreate) => {
    return await request<Task>("/tasks", { method: "POST", body: payload });
  };

  const update = async (id: number, payload: TaskUpdate) => {
    return await request<Task>(`/tasks/${id}`, { method: "PATCH", body: payload });
  };

  const remove = async (id: number) => {
    await request<void>(`/tasks/${id}`, { method: "DELETE" });
  };

  return { list, create, update, remove };
}

