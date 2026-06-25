// scripts/generate-og.mjs
// 构建时生成 OG 分享图（1200x630），覆盖所有主题
import fs from 'node:fs/promises';
import path from 'node:path';
import satori from 'satori';
import { html } from 'satori-html';
import { Resvg } from '@resvg/resvg-js';

const ROOT = path.resolve(import.meta.dirname, '..');
const OUT_DIR = path.join(ROOT, 'public', 'og');
const PUBLIC_DIR = path.join(ROOT, 'public');

const THEMES = {
  tokyo: { bg: '#1A1B26', fg: '#C0CAF5', accent: '#7AA2F7', sub: '#565F89' },
  nord:  { bg: '#2E3440', fg: '#ECEFF4', accent: '#88C0D0', sub: '#7B88A1' },
  snow:  { bg: '#ECEFF4', fg: '#2E3440', accent: '#5E81AC', sub: '#4C566A' },
};

// 1. 读取字体（用 Noto Sans SC + ZCOOL XiaoWei）
async function loadFonts() {
  // 走 CDN 缓存到本地，避免每次重下
  const cacheDir = path.join(ROOT, '.og-fonts');
  await fs.mkdir(cacheDir, { recursive: true });

  const fonts = [
    {
      name: 'NotoSansSC',
      weight: 400,
      url: 'https://fonts.gstatic.com/s/notosanssc/v36/k3kCo84MPvpLmixcA63oeAL7Iqp5IZJF9bmaG9_FnYxNbPzS5HE.119.woff2',
    },
    {
      name: 'NotoSansSC',
      weight: 700,
      url: 'https://fonts.gstatic.com/s/notosanssc/v36/k3kCo84MPvpLmixcA63oeAL7Iqp5IZJF9bmaG9_FnYxNbPzS5HE.119.woff2',
    },
  ];

  const out = [];
  for (const f of fonts) {
    const cachePath = path.join(cacheDir, `${f.name}-${f.weight}.woff2`);
    let buf;
    try {
      buf = await fs.readFile(cachePath);
    } catch {
      const res = await fetch(f.url);
      buf = Buffer.from(await res.arrayBuffer());
      await fs.writeFile(cachePath, buf);
    }
    out.push({ name: f.name, data: buf, weight: f.weight, style: 'normal' });
  }
  return out;
}

// 2. OG 图模板
function ogTemplate({ title, description, theme, url, projectTag }) {
  const t = THEMES[theme] || THEMES.tokyo;
  return `
    <div style="display:flex;flex-direction:column;width:1200px;height:630px;background:${t.bg};color:${t.fg};font-family:NotoSansSC;padding:80px;position:relative;">
      <!-- 顶部 logo + 域名 -->
      <div style="display:flex;align-items:center;gap:16px;font-size:24px;color:${t.sub};">
        <div style="width:48px;height:48px;border-radius:12px;background:${t.accent};display:flex;align-items:center;justify-content:center;color:${t.bg};font-size:32px;font-weight:700;">栗</div>
        <div>栗子糕的 BOX · lizigao-box.vercel.app</div>
      </div>

      <!-- 中间主标题 -->
      <div style="display:flex;flex-direction:column;margin-top:auto;">
        ${projectTag ? `<div style="font-size:22px;color:${t.accent};margin-bottom:24px;font-weight:700;">${projectTag}</div>` : ''}
        <div style="font-size:84px;font-weight:700;line-height:1.15;max-width:1040px;">${escapeXml(title)}</div>
        <div style="font-size:32px;color:${t.sub};margin-top:32px;line-height:1.5;max-width:1000px;">${escapeXml(description)}</div>
      </div>

      <!-- 底部装饰条 -->
      <div style="position:absolute;bottom:0;left:0;right:0;height:8px;background:linear-gradient(90deg,${t.accent} 0%,${t.accent}88 50%,${t.accent}55 100%);"></div>
    </div>
  `;
}

function escapeXml(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

// 3. 渲染 + 编码
async function renderOg({ title, description, theme, outName, projectTag }) {
  const fonts = await loadFonts();
  const markup = ogTemplate({ title, description, theme, projectTag });
  const node = html(markup);

  const svg = await satori(node, {
    width: 1200,
    height: 630,
    fonts: fonts.map(f => ({ name: f.name, data: f.data, weight: f.weight, style: f.style })),
  });

  const resvg = new Resvg(svg, {
    fitTo: { mode: 'width', value: 1200 },
  });
  const png = resvg.render().asPng();

  const outPath = path.join(OUT_DIR, `${outName}.png`);
  await fs.writeFile(outPath, png);
  console.log(`✓ ${outName}.png (${(png.length / 1024).toFixed(1)} KB)`);
}

// 4. 收集页面元数据
async function collectPages() {
  const pages = [];

  // 首页
  pages.push({
    title: '栗子糕的 BOX',
    description: '一个网友虚拟身份下的小抽屉 — 放些做过的、做着的、打算做的小东西。',
    theme: 'tokyo',
    outName: 'index',
  });

  // About
  pages.push({
    title: '关于这个站',
    description: '为什么做这个站，怎么做的，以及一些碎碎念。',
    theme: 'tokyo',
    outName: 'about',
  });

  // Data
  pages.push({
    title: '指数快照',
    description: 'A 股 + 美股主要指数收盘数据 · 每日 16:00 自动抓取',
    theme: 'nord',
    outName: 'data',
  });

  // Downloads
  pages.push({
    title: '下载中心',
    description: '桌面应用最新版本 · Windows · 含 SHA256 校验和 · 实时下载计数',
    theme: 'tokyo',
    outName: 'downloads',
  });

  // Projects
  const projects = [
    { slug: 'excel-auto-tool', name: 'Excel 自动化工具', desc: '可视化流程编辑器 + Python 执行后端' },
    { slug: 'artist-tool',     name: '画手工具箱',         desc: '截图标注 / 速写日历 / 素材管理' },
    { slug: 'multi-agent-hub', name: '智能体协作中心',   desc: '多 LLM 智能体分工：策略师 + 研究员' },
    { slug: 'rb-futures-quant',name: '螺纹钢量化策略',   desc: '基于 VNPY 框架的趋势跟踪' },
    { slug: 'stock-futures-analysis', name: '股票期货对比分析', desc: 'A 股 + 美股主要指数相关性' },
    { slug: 'index-snapshot',  name: '指数快照',           desc: '主要指数每日收盘快照' },
  ];

  for (const p of projects) {
    pages.push({
      title: p.name,
      description: p.desc,
      theme: 'snow',
      outName: `project-${p.slug}`,
      projectTag: '项目',
    });
  }

  return pages;
}

async function main() {
  await fs.mkdir(OUT_DIR, { recursive: true });
  const pages = await collectPages();
  console.log(`生成 ${pages.length} 张 OG 图...`);

  for (const p of pages) {
    await renderOg(p);
  }

  console.log(`\n✓ 完成！图都在 ${path.relative(ROOT, OUT_DIR)}/`);
}

main().catch(e => {
  console.error(e);
  process.exit(1);
});
