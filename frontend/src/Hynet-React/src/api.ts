const API_BASE = '/api/example';

export type ApiResult = {
  action?: string;
  status?: string;
  type?: string;
  loading?: number;
  num?: number;
  items?: string[] | null;
  [key: string]: unknown;
};

async function request(
  path: string,
  options: RequestInit & { body?: object } = {}
): Promise<ApiResult> {
  const { body, ...rest } = options;
  const res = await fetch(`${API_BASE}${path}`, {
    ...rest,
    headers: {
      'Content-Type': 'application/json',
      ...(rest.headers as Record<string, string>),
    },
    ...(body !== undefined && { body: JSON.stringify(body) }),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.detail ?? res.statusText);
  return data as ApiResult;
}

export const api = {
  get: (path: string) => request(path, { method: 'GET' }),
  post: (path: string, body?: object) => request(path, { method: 'POST', body }),
  delete: (path: string, body?: object) => request(path, { method: 'DELETE', body }),
};

export const endpoints = {
  symType: (type: 'standard' | 'classical') => api.post('/sym-type', { type }),
  loadType: () => api.post('/load-type'),
  disableAvr: () => api.post('/disable-avr'),
  addOvercurrentRelay: (items?: string[]) => api.post('/overcurrent-relay', { items: items ?? null }),
  removeOvercurrentRelay: (items?: string[]) => api.delete('/overcurrent-relay', { items: items ?? null }),
  addUfls: (items?: string[]) => api.post('/under-frequency-load-shedding', { items: items ?? null }),
  removeUfls: (items?: string[]) => api.delete('/under-frequency-load-shedding', { items: items ?? null }),
  addOfgt: (items?: string[]) => api.post('/over-frequency-generator-tripping', { items: items ?? null }),
  removeOfgt: (items?: string[]) => api.delete('/over-frequency-generator-tripping', { items: items ?? null }),
  addUfgt: (items?: string[]) => api.post('/under-frequency-generator-tripping', { items: items ?? null }),
  removeUfgt: (items?: string[]) => api.delete('/under-frequency-generator-tripping', { items: items ?? null }),
  generatorControl: () => api.post('/generator-control'),
  loadingLevel: (loading: number) => api.post('/loading-level', { loading }),
  initialGenerationLevel: (loading: number) => api.post('/initial-generation-level', { loading }),
  lineRating: () => api.post('/line-rating'),
  randomCases: (num: number) => api.post('/random-cases', { num }),
  runN2Contingencies: () => api.post('/run-n2-contingencies'),
  matching: () => api.post('/matching'),
  simulation: () => api.get('/simulation'),
};
