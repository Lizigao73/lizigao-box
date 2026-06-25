// 站点常量
export const SITE = {
  name: '栗子糕的BOX',
  shortName: '栗子糕BOX',
  description: '一个网友虚拟身份下的作品集合——桌面应用、数据追踪、AI 实验，想到啥就做啥。',
  url: 'https://lizigao-box.vercel.app',
  locale: 'zh-CN',
  // 反馈邮箱（如需启用可去掉注释）
  // email: 'hello@lizigao-box.vercel.app',
  // 社交链接（如有）
  social: [
    // { name: 'GitHub', url: 'https://github.com/lizigao-box', icon: 'github' },
  ],
} as const;

export const NAV = [
  { label: '首页',  href: '/' },
  { label: '项目',  href: '/#projects' },
  { label: '数据',  href: '/data' },
  { label: '下载',  href: '/downloads' },
  { label: '关于',  href: '/about' },
] as const;

// 状态元信息
export const STATUS_META = {
  shipped:    { label: '成品',     color: 'moss',  zh: '已发布' },
  building:   { label: '开发中',   color: 'amber', zh: '持续迭代' },
  experiment: { label: '实验中',   color: 'iris',  zh: '验证想法' },
  online:     { label: '在线追踪', color: 'sky',   zh: '持续更新' },
} as const;

export const CATEGORY_META = {
  desktop: { label: '桌面应用', icon: 'monitor' },
  data:    { label: '数据追踪', icon: 'chart' },
  ai:      { label: 'AI 实验',  icon: 'sparkles' },
  other:   { label: '其它',     icon: 'package' },
} as const;

export type Status = keyof typeof STATUS_META;
export type Category = keyof typeof CATEGORY_META;

// ===========================================================
// Giscus 评论（GitHub Discussions）
// 在 https://giscus.app/zh-CN 填好仓库和分类，把生成的值填到下面
// 字段为空则评论区不渲染
// ===========================================================
export const GISCUS = {
  /** GitHub 仓库，格式：用户名/仓库名 */
  repo: 'lizigao/lizigao-box',
  /** 仓库 ID（giscus.app 给你） */
  repoId: 'R_PLACEHOLDER',
  /** Discussion 分类名 */
  category: 'Announcements',
  /** 分类 ID */
  categoryId: 'DIC_PLACEHOLDER',
} as const;

// ===========================================================
// Plausible 统计
// 注册 https://plausible.io 后填入注册的域名
// 留空则不加载 Plausible 脚本
// ===========================================================
export const PLAUSIBLE_DOMAIN = ''; // e.g. 'lizigao-box.pages.dev'

// ===========================================================
// 站点构建元数据
// ===========================================================
export const BUILD_INFO = {
  /** 网站部署平台（Vercel / Cloudflare Pages / Netlify） */
  platform: 'Cloudflare Pages' as 'Vercel' | 'Cloudflare Pages' | 'Netlify' | 'GitHub Pages',
  /** 部署域名 */
  domain: 'lizigao-box.pages.dev',
  /** 仓库地址 */
  repoUrl: 'https://github.com/lizigao/lizigao-box',
} as const;
