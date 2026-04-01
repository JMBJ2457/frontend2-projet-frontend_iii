const BASE = import.meta.env.VITE_API_URL || '/api';

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    ...options,
  });
  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(text || `HTTP ${res.status}`);
  }
  if (res.status === 204) return undefined as T;
  return res.json() as Promise<T>;
}

export const api = {
  departamentos: {
    list: () => request<any[]>(`/departamentos/`),
    create: (body: { nombre: string; prioridad: 'low' | 'medium' | 'high'; proxima_revision?: string | null; descripcion?: string | null; }) =>
      request<any>(`/departamentos/`, { method: 'POST', body: JSON.stringify(body) }),
    changePriority: (id: string, prioridad: 'low' | 'medium' | 'high') =>
      request<any>(`/departamentos/${id}/prioridad?prioridad=${encodeURIComponent(prioridad)}`, { method: 'PATCH' }),
    update: (id: string, body: Partial<{ nombre: string; prioridad: 'low' | 'medium' | 'high'; proxima_revision?: string | null; descripcion?: string | null }>) =>
      request<any>(`/departamentos/${encodeURIComponent(id)}`, { method: 'PUT', body: JSON.stringify(body) }),
    delete: (id: string) => request<void>(`/departamentos/${encodeURIComponent(id)}`, { method: 'DELETE' }),
  },
  equipos: {
    list: (params?: { department_id?: string; unassigned_only?: boolean }) => {
      const qs: string[] = [];
      if (params?.department_id) qs.push(`department_id=${encodeURIComponent(params.department_id)}`);
      if (params?.unassigned_only) qs.push(`unassigned_only=true`);
      const query = qs.length ? `?${qs.join('&')}` : '';
      return request<any[]>(`/equipos/${query}`);
    },
    count: () => request<number>(`/equipos/count`),
    get: (id: string) => request<any>(`/equipos/${encodeURIComponent(id)}`),
    create: (body: any) => request<any>(`/equipos/`, { method: 'POST', body: JSON.stringify(body) }),
    update: (id: string, body: any) => request<any>(`/equipos/${id}`, { method: 'PUT', body: JSON.stringify(body) }),
  },
  positions: {
    list: (department_id?: string) =>
      request<any[]>(`/puestos/${department_id ? `?department_id=${encodeURIComponent(department_id)}` : ''}`),
    create: (body: { nombre: string; department_id: string; nivel_uso?: 'low' | 'medium' | 'high' }) =>
      request<any>(`/puestos/`, { method: 'POST', body: JSON.stringify(body) }),
    update: (id: string, body: Partial<{ nombre: string; nivel_uso: 'low' | 'medium' | 'high'; department_id: string }>) =>
      request<any>(`/puestos/${encodeURIComponent(id)}`, { method: 'PUT', body: JSON.stringify(body) }),
    delete: (id: string) =>
      request<void>(`/puestos/${encodeURIComponent(id)}`, { method: 'DELETE' }),
  },
  usuarios: {
    list: () => request<any[]>(`/usuarios/`),
    get: (id: string) => request<any>(`/usuarios/${encodeURIComponent(id)}`),
  },
  maintenance: {
    upcoming: (params?: { week?: string; tipo?: 'operacional' | 'laboratorio'; limit?: number; autogen?: boolean }) => {
      const qs: string[] = [];
      if (params?.week) qs.push(`week=${encodeURIComponent(params.week)}`);
      if (params?.tipo) qs.push(`tipo=${encodeURIComponent(params.tipo)}`);
      if (params?.limit) qs.push(`limit=${encodeURIComponent(String(params.limit))}`);
      if (typeof params?.autogen === 'boolean') qs.push(`autogen=${params.autogen ? 'true' : 'false'}`);
      const query = qs.length ? `?${qs.join('&')}` : '';
      return request<any[]>(`/maintenance/upcoming${query}`);
    },
    schedule: (count = 3, tipo: 'operacional' | 'laboratorio' = 'operacional') =>
      request<any[]>(`/maintenance/schedule?count=${encodeURIComponent(String(count))}&tipo=${encodeURIComponent(tipo)}`, { method: 'POST' }),
    complete: (id: string) => request<any>(`/maintenance/${encodeURIComponent(id)}/complete`, { method: 'POST' }),
    kpis: (week?: string) => request<any>(`/maintenance/kpis${week ? `?week=${encodeURIComponent(week)}` : ''}`),
    statsYearly: () => request<any>(`/maintenance/stats-yearly`),
    advanceWeek: (week?: string) =>
      request<any>(`/maintenance/advance-week${week ? `?week=${encodeURIComponent(week)}` : ''}`, { method: 'POST' }),
    practicantes: {
      // Backward-compat shim pointing to new RESTful endpoints
      list: () => request<any[]>(`/practicantes/`),
      create: (body: { nombre: string; cuatrimestre?: string; prioridad?: 'alta' | 'media' | 'baja'; activo?: boolean }) =>
        request<any>(`/practicantes/`, { method: 'POST', body: JSON.stringify(body) }),
      update: (id: string, body: Partial<{ nombre: string; cuatrimestre: string; prioridad: 'alta' | 'media' | 'baja'; activo: boolean }>) =>
        request<any>(`/practicantes/${encodeURIComponent(id)}`, { method: 'PUT', body: JSON.stringify(body) }),
      disponibilidades: {
        create: (body: { practicante_id: string; day_of_week: number; hora_inicio: string; hora_fin: string; disponible_en_vacaciones?: boolean; disponible_fin_de_semana?: boolean; }) =>
          request<any>(`/practicantes/disponibilidades`, { method: 'POST', body: JSON.stringify(body) }),
        listByPracticante: (practicante_id: string) =>
          request<any[]>(`/practicantes/${encodeURIComponent(practicante_id)}/disponibilidades`),
        replace: (practicante_id: string, items: Array<{ day_of_week: number; hora_inicio: string; hora_fin: string; disponible_en_vacaciones?: boolean; disponible_fin_de_semana?: boolean }>) =>
          request<any[]>(`/practicantes/${encodeURIComponent(practicante_id)}/disponibilidades`, { method: 'PUT', body: JSON.stringify({ items }) }),
      },
    },
    assignPracticante: (maintenance_id: string, practicante_id: string) =>
      request<any>(`/maintenance/${encodeURIComponent(maintenance_id)}/assign-practicante?practicante_id=${encodeURIComponent(practicante_id)}`, { method: 'POST' }),
  },
  practicantes: {
    list: () => request<any[]>(`/practicantes/`),
    create: (body: { nombre: string; cuatrimestre?: string; prioridad?: 'alta' | 'media' | 'baja'; activo?: boolean }) =>
      request<any>(`/practicantes/`, { method: 'POST', body: JSON.stringify(body) }),
    update: (id: string, body: Partial<{ nombre: string; cuatrimestre: string; prioridad: 'alta' | 'media' | 'baja'; activo: boolean }>) =>
      request<any>(`/practicantes/${encodeURIComponent(id)}`, { method: 'PUT', body: JSON.stringify(body) }),
    disponibilidades: {
      create: (body: { practicante_id: string; day_of_week: number; hora_inicio: string; hora_fin: string; disponible_en_vacaciones?: boolean; disponible_fin_de_semana?: boolean; }) =>
        request<any>(`/practicantes/disponibilidades`, { method: 'POST', body: JSON.stringify(body) }),
      listByPracticante: (practicante_id: string) =>
        request<any[]>(`/practicantes/${encodeURIComponent(practicante_id)}/disponibilidades`),
      replace: (practicante_id: string, items: Array<{ day_of_week: number; hora_inicio: string; hora_fin: string; disponible_en_vacaciones?: boolean; disponible_fin_de_semana?: boolean }>) =>
        request<any[]>(`/practicantes/${encodeURIComponent(practicante_id)}/disponibilidades`, { method: 'PUT', body: JSON.stringify({ items }) }),
    },
  },
};
