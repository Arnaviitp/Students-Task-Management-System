export function useApi() {
  const config = useRuntimeConfig();
  const baseURL = config.public.apiBase as string;

  const request = async <T>(path: string, options: any = {}): Promise<T> => {
    return await $fetch<T>(path, { baseURL, ...options });
  };

  return { baseURL, request };
}

