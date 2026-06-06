const BASE = "/api";

async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(url, {
    headers: { "Content-Type": "application/json", ...options?.headers },
    ...options,
  });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`${res.status}: ${body || res.statusText}`);
  }
  if (res.status === 204) return undefined as T;
  return res.json();
}

// ---------- Functions ----------
export const functionApi = {
  list: (projectId: string) => request<any[]>(`${BASE}/projects/${projectId}/functions`),
  get: (id: string) => request<any>(`${BASE}/functions/${id}`),
  create: (projectId: string, body: any) =>
    request<any>(`${BASE}/projects/${projectId}/functions`, { method: "POST", body: JSON.stringify(body) }),
  update: (id: string, body: any) =>
    request<any>(`${BASE}/functions/${id}`, { method: "PATCH", body: JSON.stringify(body) }),
  delete: (id: string) => request<void>(`${BASE}/functions/${id}`, { method: "DELETE" }),
};

// ---------- SCs ----------
export const scApi = {
  list: (projectId: string) => request<any[]>(`${BASE}/projects/${projectId}/scs`),
  get: (id: string) => request<any>(`${BASE}/scs/${id}`),
  create: (projectId: string, body: any) =>
    request<any>(`${BASE}/projects/${projectId}/scs`, { method: "POST", body: JSON.stringify(body) }),
  update: (id: string, body: any) =>
    request<any>(`${BASE}/scs/${id}`, { method: "PATCH", body: JSON.stringify(body) }),
  delete: (id: string) => request<void>(`${BASE}/scs/${id}`, { method: "DELETE" }),
};

// ---------- SSCs ----------
export const sscApi = {
  list: (scId: string) => request<any[]>(`${BASE}/scs/${scId}/sscs`),
  get: (id: string) => request<any>(`${BASE}/sscs/${id}`),
  create: (scId: string, body: any) =>
    request<any>(`${BASE}/scs/${scId}/sscs`, { method: "POST", body: JSON.stringify(body) }),
  update: (id: string, body: any) =>
    request<any>(`${BASE}/sscs/${id}`, { method: "PATCH", body: JSON.stringify(body) }),
  delete: (id: string) => request<void>(`${BASE}/sscs/${id}`, { method: "DELETE" }),
};

// ---------- ECUs ----------
export const ecuApi = {
  list: (projectId: string) => request<any[]>(`${BASE}/projects/${projectId}/ecus`),
  get: (id: string) => request<any>(`${BASE}/ecus/${id}`),
  create: (projectId: string, body: any) =>
    request<any>(`${BASE}/projects/${projectId}/ecus`, { method: "POST", body: JSON.stringify(body) }),
  update: (id: string, body: any) =>
    request<any>(`${BASE}/ecus/${id}`, { method: "PATCH", body: JSON.stringify(body) }),
  delete: (id: string) => request<void>(`${BASE}/ecus/${id}`, { method: "DELETE" }),
};

// ---------- Signals ----------
export const signalApi = {
  list: (sscId: string) => request<any[]>(`${BASE}/sscs/${sscId}/signals`),
  get: (id: string) => request<any>(`${BASE}/signals/${id}`),
  create: (sscId: string, body: any) =>
    request<any>(`${BASE}/sscs/${sscId}/signals`, { method: "POST", body: JSON.stringify(body) }),
  update: (id: string, body: any) =>
    request<any>(`${BASE}/signals/${id}`, { method: "PATCH", body: JSON.stringify(body) }),
  delete: (id: string) => request<void>(`${BASE}/signals/${id}`, { method: "DELETE" }),
};

// ---------- Baselines ----------
export const baselineApi = {
  list: (projectId: string) => request<any[]>(`${BASE}/projects/${projectId}/baselines`),
  get: (id: string) => request<any>(`${BASE}/baselines/${id}`),
  create: (projectId: string, body: any) =>
    request<any>(`${BASE}/projects/${projectId}/baselines`, { method: "POST", body: JSON.stringify(body) }),
  update: (id: string, body: any) =>
    request<any>(`${BASE}/baselines/${id}`, { method: "PATCH", body: JSON.stringify(body) }),
  delete: (id: string) => request<void>(`${BASE}/baselines/${id}`, { method: "DELETE" }),
  items: {
    list: (baselineId: string) => request<any[]>(`${BASE}/baselines/${baselineId}/items`),
    create: (baselineId: string, body: any) =>
      request<any>(`${BASE}/baselines/${baselineId}/items`, { method: "POST", body: JSON.stringify(body) }),
  },
};

// ---------- CCPs ----------
export const ccpApi = {
  list: (sscId: string) => request<any[]>(`${BASE}/sscs/${sscId}/ccps`),
  get: (id: string) => request<any>(`${BASE}/ccps/${id}`),
  create: (sscId: string, body: any) =>
    request<any>(`${BASE}/sscs/${sscId}/ccps`, { method: "POST", body: JSON.stringify(body) }),
  update: (id: string, body: any) =>
    request<any>(`${BASE}/ccps/${id}`, { method: "PATCH", body: JSON.stringify(body) }),
  delete: (id: string) => request<void>(`${BASE}/ccps/${id}`, { method: "DELETE" }),
};

// ---------- Trace Matrix ----------
export const traceApi = {
  matrix: (projectId: string) => request<any>(`${BASE}/projects/${projectId}/trace-matrix`),
};
