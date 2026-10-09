import { randomUUID } from 'node:crypto';
const base = 'https://soldfetch.com';
const allowed = /^\/(?:v1\/scrape(?:\/category)?|v1\/item\/[0-9]{9,15}|usage|requests|v1\/capabilities)$/;
export async function get(path, params = {}, {key = process.env.SOLDFETCH_API_KEY, idempotencyKey = randomUUID(), fetchImpl = fetch} = {}) {
  if (!allowed.test(path)) throw new Error('Unsupported SoldFetch path');
  if (!key?.trim()) throw new Error('Set SOLDFETCH_API_KEY');
  const url = new URL(path, base);
  for (const [name, value] of Object.entries(params)) if (value !== undefined && value !== null) url.searchParams.set(name, String(value));
  const response = await fetchImpl(url, {
    headers: {Authorization: `Bearer ${key.trim()}`, Accept: 'application/json', 'Idempotency-Key': idempotencyKey},
    redirect: 'error', signal: AbortSignal.timeout(65000),
  });
  if (!response.ok) throw new Error(`SoldFetch HTTP ${response.status}; request ID: ${response.headers.get('x-request-id') || 'unavailable'}`);
  return response.json();
}
