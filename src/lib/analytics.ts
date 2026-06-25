// src/lib/analytics.ts
// Plausible 自定义事件追踪
// Plausible 通过 window.plausible(name, { props }) 记录事件
// 仅在加载了 Plausible 脚本时才生效

declare global {
  interface Window {
    plausible?: (name: string, options?: { props?: Record<string, string | number> }) => void;
  }
}

export function trackEvent(name: string, props?: Record<string, string | number>) {
  if (typeof window === 'undefined') return;
  if (typeof window.plausible !== 'function') return;
  try {
    window.plausible(name, props ? { props } : undefined);
  } catch {
    // 静默失败
  }
}

// 预定义事件名
export const EVENTS = {
  DOWNLOAD: 'download',
  THEME_CHANGE: 'theme_change',
  PROJECT_VIEW: 'project_view',
  EXTERNAL_LINK: 'external_link',
  COMMENT_POST: 'comment_post',
} as const;
