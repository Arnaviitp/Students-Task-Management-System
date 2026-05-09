export type TaskStatus = "todo" | "in_progress" | "done";

export type Task = {
  id: number;
  title: string;
  description: string | null;
  status: TaskStatus;
  priority: 1 | 2 | 3;
  due_date: string | null;
  created_at: string;
  updated_at: string;
};

export type TaskCreate = {
  title: string;
  description?: string | null;
  status?: TaskStatus;
  priority?: 1 | 2 | 3;
  due_date?: string | null;
};

export type TaskUpdate = Partial<TaskCreate>;

