// src/pages/api/download/[id].ts
// 下载中转：记录下载数 → 重定向到文件
import type { APIRoute } from 'astro';
import { findDownload } from '../../../lib/downloads';

export const prerender = false; // 必须是 serverless function

export const GET: APIRoute = async ({ params, request }) => {
  const id = params.id;
  if (!id) return new Response('Missing id', { status: 400 });

  const entry = findDownload(id);
  if (!entry) return new Response('Not found', { status: 404 });

  // 1. 记录下载（Vercel KV / Cloudflare KV / Upstash Redis 都可）
  try {
    await incrementCounter(id);
  } catch (e) {
    console.error('计数失败:', e);
    // 不阻塞下载
  }

  // 2. 触发 Plausible 自定义事件（如果加载了）
  //    Plausible 会在前端通过 plausible() 调用记录

  // 3. 302 重定向到文件
  const fileUrl = entry.storage === 'blob' && entry.blobUrl
    ? entry.blobUrl
    : `/downloads/${entry.filename}`;

  return new Response(null, {
    status: 302,
    headers: {
      'Location': fileUrl,
      'Cache-Control': 'no-cache, no-store, must-revalidate',
    },
  });
};

async function incrementCounter(id: string): Promise<number> {
  // 方案 A：Vercel KV（推荐）
  // import { kv } from '@vercel/kv';
  // const count = await kv.incr(`download:${id}`);
  // return count;

  // 方案 B：Upstash Redis（HTTP API，免连接配置）
  const url = process.env.UPSTASH_REDIS_REST_URL;
  const token = process.env.UPSTASH_REDIS_REST_TOKEN;
  if (url && token) {
    const res = await fetch(`${url}/incr/download:${id}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (res.ok) {
      const data = await res.json();
      return Number(data.result || 0);
    }
  }

  // 方案 C：兜底 - 写本地文件（dev only）
  // await writeLocalCounter(id);
  return 0;
}
