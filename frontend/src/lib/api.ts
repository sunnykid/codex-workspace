import { clearToken, getToken, setToken } from "./auth";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL?.toString() || "http://localhost:8000";

export type FileItem = {
  id: number;
  original_filename: string;
  content_type?: string | null;
  size_bytes: number;
  tags?: string[] | null;
  created_at: string;
};

export type PaginatedResponse = {
  items: FileItem[];
  total: number;
  limit: number;
  offset: number;
};

const redirectToLogin = () => {
  clearToken();
  window.location.assign("/login");
};

const parseErrorMessage = async (response: Response) => {
  try {
    const data = await response.json();
    if (data?.detail) {
      return data.detail as string;
    }
  } catch {
    // Ignore JSON parse errors.
  }
  return response.statusText || "요청 중 오류가 발생했습니다.";
};

const apiFetch = async (path: string, options: RequestInit = {}) => {
  const token = getToken();
  const headers = new Headers(options.headers ?? {});
  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers,
  });

  if (response.status === 401) {
    redirectToLogin();
    throw new Error("인증이 필요합니다.");
  }

  if (!response.ok) {
    const message = await parseErrorMessage(response);
    throw new Error(message);
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
};

export const register = async (email: string, password: string) => {
  return apiFetch("/auth/register", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password }),
  });
};

export const login = async (email: string, password: string) => {
  const data = await apiFetch("/auth/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password }),
  });
  if (data?.access_token) {
    setToken(data.access_token);
  }
  return data;
};

export const listFiles = async (limit: number, offset: number) => {
  return apiFetch(`/files?limit=${limit}&offset=${offset}`) as Promise<PaginatedResponse>;
};

export const uploadFile = async (file: File, tags: string[]) => {
  const formData = new FormData();
  formData.append("upload", file);
  if (tags.length > 0) {
    formData.append("tags", JSON.stringify(tags));
  }

  return apiFetch("/files", {
    method: "POST",
    body: formData,
  });
};

export const deleteFile = async (id: number) => {
  return apiFetch(`/files/${id}`, {
    method: "DELETE",
  });
};

export const searchFiles = async (
  q: string,
  tag: string,
  limit: number,
  offset: number
) => {
  const params = new URLSearchParams();
  if (q) {
    params.set("q", q);
  }
  if (tag) {
    params.set("tag", tag);
  }
  params.set("limit", limit.toString());
  params.set("offset", offset.toString());

  return apiFetch(`/search?${params.toString()}`) as Promise<PaginatedResponse>;
};

export const downloadUrl = (id: number) => {
  return `${API_BASE_URL}/files/${id}/download`;
};
