/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,ts,tsx,vue,svelte}'],
  darkMode: ['selector', '[data-theme="tokyo"], [data-theme="nord"]'],
  theme: {
    extend: {
      colors: {
        // 语义化 token —— 全部指向 CSS 变量，主题切换时自动跟随
        bg: {
          primary:   'var(--bg-primary)',
          secondary: 'var(--bg-secondary)',
          tertiary:  'var(--bg-tertiary)',
          // 玻璃卡专用：仅 synthwave 用 rgba，其它主题会由变量重写为不透明
          glass:     'var(--bg-glass)',
        },
        text: {
          primary:   'var(--text-primary)',
          secondary: 'var(--text-secondary)',
          tertiary:  'var(--text-tertiary)',
        },
        border: {
          DEFAULT: 'var(--border)',
          soft:    'var(--border-soft)',
        },
        accent: {
          DEFAULT: 'var(--accent)',
          hover:   'var(--accent-hover)',
          // 用于渐变文字
          gradient: 'var(--accent-gradient)',
        },
        status: {
          shipped:    'var(--status-shipped)',
          building:   'var(--status-building)',
          experiment: 'var(--status-experiment)',
          online:     'var(--status-online)',
          down:       'var(--status-down)',
        },
        // 指数涨跌色（A 股习惯：涨红跌绿）
        index: {
          up:   'var(--index-up)',
          down: 'var(--index-down)',
        },
        // 向后兼容旧类名（consts.ts 内部还在用 moss/amber/iris/sky 作为逻辑名）
        // 这些 className 在主题切换时仍会跟随变量走
        moss:    'var(--status-shipped)',
        amber:   'var(--status-building)',
        iris:    'var(--status-experiment)',
        sky:     'var(--status-online)',
      },
      fontFamily: {
        display: ['"ZCOOL XiaoWei"', '"Noto Serif SC"', 'Georgia', 'serif'],
        serif:   ['"Noto Serif SC"', 'Georgia', 'serif'],
        sans:    ['"Noto Sans SC"', 'system-ui', 'sans-serif'],
        mono:    ['"JetBrains Mono"', 'ui-monospace', 'monospace'],
      },
      borderRadius: {
        card: '14px',
        pill: '999px',
      },
      boxShadow: {
        // 主题相关的柔和阴影
        soft:    '0 2px 8px var(--shadow-color)',
        'soft-lg':'0 8px 28px var(--shadow-color)',
        glow:    '0 0 0 1px var(--accent-soft), 0 8px 24px var(--accent-glow)',
      },
      animation: {
        'pulse-slow': 'pulse 3.5s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'fade-up':    'fadeUp 0.6s ease-out both',
        'stagger':    'staggerIn 0.5s ease-out both',
      },
      keyframes: {
        fadeUp: {
          '0%':   { opacity: '0', transform: 'translateY(8px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        staggerIn: {
          '0%':   { opacity: '0', transform: 'translateY(12px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
};
