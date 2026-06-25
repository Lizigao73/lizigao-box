// src/pages/api/downloads/count.ts
// 获取下载计数（公开 GET，前端用）
import type { APIRoute } from 'astro';
import { DOWNLOADS } from '../../../lib/downloads';

export const prerender = false;

export const GET: APIRoute = async () => {
  const ids = DOWNLOADS.map(d => d.id);
  const counts: Record<string, number> = {};

  const url = process.env.UPSTASH_REDIS_REST_URL;
  const token = process.env.UPSTASH_REDIS_REST_TOKEN;

  if (url && token) {
    // 批量取
    const res = await fetch(`${url}/mget?${ids.map(id => `download:${id}`).join('&')}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (res.ok) {
      const data = await res.json();
      const values = data.result || [];
      ids.forEach((id, i) => {
        counts[id] = Number(values[i] || 0);
      });
    }
  } else {
    // 兜底 - 全 0
    ids.forEach(id => { counts[id] = 0; });
  }

  return new Response(JSON.stringify({ counts, updatedAt: new Date().toISOString() }), {
    status: 200,
    headers: {
      'Content-Type': 'application/json',
      'Cache-Control': 'public, max-age=30, stale-while-revalidate=300',
    },
  });
};
