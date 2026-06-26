# 栗子糕的BOX · 产品需求文档（PRD）

> **项目代号**：lizigao-box
> **在线地址**：https://lizigao-box.pages.dev
> **部署平台**：Cloudflare Pages（Git 集成 · push 自动部署）
> **最后更新**：2026-06-27

---

## 1. 项目定位

一个**个人作品集 + 数据追踪**的单页门户，主要服务于：

- 展示个人项目（excle-auto-tool、rb-futures-quant、index-snapshot 等）
- 自动抓取并展示 A 股 / 美股 / 黄金 / 美元指数每日收盘价
- 提供作品 / 软件下载、订阅 RSS

视觉系统走 Tokyo Night → Nord → Snow 三套主题，强调**日式极简**与**工程感**字体（ZCOOL XiaoWei 标题 + JetBrains Mono 数据）。

---

## 2. 核心功能模块

### 2.1 首页 `/`
- Hero 区：标题、副标题、实时时钟（HeroClock 组件）
- 项目卡片网格（按 `src/content/projects/*.md` 生成）
- 主题切换器（平铺色块，3 选项）

### 2.2 数据追踪 `/data`  ⭐ 本次主要迭代
- **当日卡片**（不受日期范围影响，永远显示最新一日）
  - 上证 / 深证 / 标普 500 / 纳斯达克 / 伦敦黄金 / 美元指数
  - 涨跌色：A 股习惯 —— 涨红 `#F7768E`、跌绿 `#9ECE6A`（三套主题均定义 `--index-up` / `--index-down` 变量）
- **日期范围选择器**（同时驱动图表 + 表格）
  - 两个 `<input type="date">` + 4 个预设按钮：近 1 月 / 近 3 月 / 近 6 月 / 全部
  - 默认范围：最近 30 个交易日
- **趋势图**（Chart.js 4.x）
  - 图 1：A 股 + 美股（4 条线，双 Y 轴：左 A 股，右美股）
  - 图 2：伦敦黄金 + 美元指数（双 Y 轴：左 USD/oz，右 DXY）
  - 主题色通过 CSS 变量动态读取，切换主题时图表配色随之更新
- **历史快照表格**
  - 外层 `max-height: 480px` + `overflow-y: auto`，避免页面过长
  - `<thead>` 用 `sticky top-0` 固定表头
  - 行 `data-date` 标记；日期范围变化时通过 `display:none` 隐藏范围外行
  - 顶部显示「显示 N / M 条」

### 2.3 项目详情 `/projects/[slug]`
- 从 `src/content/projects/*.md` 加载，渲染 frontmatter + body
- 含 StatusBadge、CategoryChip、Comments

### 2.4 下载 `/downloads`
- 列出可下载的二进制 / 脚本
- 通过 `/api/download/[id].ts` 计数 + 重定向

### 2.5 其它
- `/about`、`/rss.xml`、`/sitemap`、`/404`

---

## 3. 主题系统

| 主题 | data-theme | 配色基色 | 用途 |
|------|-----------|----------|------|
| Tokyo Night | `tokyo` | 深蓝紫 #1A1B26 + 蓝紫 #7AA2F7 | **默认主题**（不管系统 light/dark） |
| Nord Polar  | `nord`  | 极地寒冰 #2E3440 + 冰蓝 #88C0D0 | 备选深色 |
| Snow Tundra | `snow`  | 雪原浅 #ECEFF4 + 钢蓝 #5E81AC | 备选浅色 |

主题变量在 `src/styles/global.css` 的 `:root` / `[data-theme="nord"]` / `[data-theme="snow"]` 三个 block 中分别定义。

**Anti-FOUC 策略**：在 `<head>` 第一个 inline 脚本读 localStorage → 立即设置 `data-theme`。**默认无 localStorage 时一律 Tokyo**（不再跟随系统深浅模式）。

主题选择持久化在 `localStorage('lizigao-box-theme')`。

---

## 4. 数据流

### 4.1 数据文件
`src/data/financial-snapshots.json`：
```json
{
  "lastUpdated": "ISO 8601 +08:00",
  "source": "...",
  "note": "...",
  "snapshots": [
    { "date": "YYYY-MM-DD", "shIndex": ..., "szIndex": ..., "sp500": ..., "nasdaq": ..., "gold": ..., "dxy": ..., "fetchedAt": "..." }
  ]
}
```

### 4.2 抓取流程
GitHub Actions `daily-fetch.yml`：
- 触发：每天 UTC 8:00（北京时间 16:00）+ workflow_dispatch
- 步骤：
  1. checkout
  2. 装 akshare + yfinance
  3. `python scripts/fetch_snapshots.py`：取今日 6 个指数
  4. 追加 / 覆盖到 `financial-snapshots.json`
  5. 检测到变更则 `git commit` + `git push`（带 `[skip ci]` 防止触发部署循环）

### 4.3 回溯（一次性）
`scripts/backfill_history.py`：用带噪声的 smoothstep 路径，从锚点（2026-05-14 真实收盘）反推补全到 2026-01-09，约 90 个交易日。

---

## 5. 工程约定

- **Framework**: Astro 5.x（静态站点，hybrid output）
- **CSS**: Tailwind 3.4 + `src/styles/global.css`（CSS 变量层）
- **TypeScript**: strict mode，`src/types/*.ts` 定义所有领域模型
- **字体**: Google Fonts（ZCOOL XiaoWei + Noto Serif SC + Noto Sans SC + JetBrains Mono）
- **图表**: Chart.js 4.x（手动注册需要的 components，避免 tree-shaking 失效）
- **包管理**: npm + `package-lock.json`（生产构建用 `npm ci`）
- **部署**: Cloudflare Pages，框架预设 Astro，build command `npm run build`，output `dist`

### 工程约束
- 所有 panel 配置面板中，颜色直接走 CSS 变量（`var(--xxx)`），不写死 hex
- `<input type="date">` 必须带 `min` / `max` 限制可选范围
- 表格表头必须用 `sticky top-0` 以便长表滚动
- Chart.js 数据点 > 50 时建议关闭 `animation`（已在 `data.astro` 设置 `animation: false`）

---

## 6. 部署 & 清理清单

### 6.1 已完成清理
- ✅ 删除 GitHub Actions 部署 workflow（改用 Cloudflare Git 集成）
- ✅ 删除重复的 `fetch-snapshots.yml`（保留 `daily-fetch.yml`）
- ✅ 清理旧 Workers 项目（每月省 11 build mins）
- ✅ 清理 GitHub Secrets `CLOUDFLARE_API_TOKEN` / `CLOUDFLARE_ACCOUNT_ID`

### 6.2 当前 GitHub Actions
| Workflow | 用途 |
|----------|------|
| `build.yml` | push main → 跑 `astro check` + `npm run build` 上传 dist artifact（备份） |
| `build-verify.yml` | PR → 类型检查 + 构建 |
| `daily-fetch.yml` | 每日 16:00 抓取指数 + 提交数据 |

### 6.3 Cloudflare Pages 配置
- 项目名：`lizigao-box`
- 框架：Auto-detected → Astro
- Build command：`npm run build`
- Output：`dist`
- 环境变量：（无）

---

## 7. 路线图

### 已完成
- [x] 默认 Tokyo 主题（不跟随系统）
- [x] 涨跌色反转：涨红跌绿（三主题适配）
- [x] 新增伦敦黄金 + 美元指数
- [x] 数据回溯至 2026-01（120 个交易日）
- [x] 日期范围选择器（图表 + 表格联动）
- [x] 历史表格可滚动 + sticky 表头
- [x] 图表默认显示近 1 月
- [x] 快速范围按钮：1M / 3M / 6M / 全部
- [x] 重复 workflow 清理

### 未来
- [ ] 引入 `chartjs-plugin-zoom` 提供图表内拖拽缩放
- [ ] 增加更多指数（恒生、原油、比特币）
- [ ] 月度 / 季度对比视图
- [ ] PWA 离线缓存
- [ ] RSS 增量触发（数据更新时生成）
