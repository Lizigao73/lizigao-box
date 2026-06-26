# 数据源整顿 · 部署说明

## 根本原因
线上数据错误是 **GitHub Actions 的问题**：
- `daily-fetch.yml` 之前调用 `fetch_snapshots.py`（用 yfinance）
- yfinance 国内网络限速，每次抓取都失败
- Cloudflare Pages 部署了失败前的最后一次成功数据（数据陈旧/错误）

## 已完成的本地修复（commit hash: 01f19f5）

### 1. 数据源切换（全部官方/权威）
| 指数 | 新源 |
|---|---|
| 上证/深证 | `akshare.stock_zh_index_daily` → 新浪财经 |
| 标普500/纳指 | `akshare.index_us_stock_sina(.INX/.IXIC)` |
| 伦敦金 XAU | `akshare.futures_foreign_hist` |
| 美元指数 DXY | sina hq DINI（实时） |

### 2. daily-fetch.yml 改造
- 弃用 yfinance 路径，调用 `fetch_official.py`
- 新增 `pip install akshare` 步骤
- 移除已失效的 `fetch-snapshots.yml`

### 3. 数据验证（6/26 本地实测）
```
上证指数   = 4027.265   ← 用户验证点 ✅
伦敦金    = 4067.45    ← 用户验证点 ✅
标普 500  = 7357.49
纳指      = 25358.60
DXY       = 101.35
共 268 条历史（2025-06-17 → 2026-06-26）
```

### 4. 前端优化（同一 commit）
- chartjs-plugin-zoom：图表支持拖拽缩放/滚轮缩放/双击重置
- Google Fonts 精简：Noto Sans SC 只保留 400/600（砍 3 个字重）
- IndexedDB 缓存：首次写入 `lizigao-box` DB，后续跳过 JSON.parse

## 需要你做的（沙箱网络无法 push 到 GitHub）

请在 **本机 PowerShell / Git Bash**（不是 Trae 沙箱）执行：

```bash
cd "D:\Interest\Trae\lizigao-box"
git push origin main
```

push 成功后：
1. Cloudflare Pages 会通过 Git 集成自动触发部署（1-3 分钟）
2. 部署完成后访问 https://lizigao-box.pages.dev/data 即可看到 6/26 真实数据
3. 此后每天 UTC 8:00（北京时间 16:00）GitHub Actions 自动抓取最新数据

## 构建验证（已通过）
- `npm run build`：✅ 0 错误
- `npm run check`：✅ 0 错误 0 警告
