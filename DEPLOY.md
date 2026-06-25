# 🚀 部署 Todo List

> 部署到 Cloudflare Pages（国内访问最快的免费方案）。
> 我会标记每项是谁负责、你操作时遇到问题随时问我。

## 阶段 1：基础部署（~10 分钟）

### 1.1 推 GitHub 🤚 你操作

```bash
cd d:\Interest\Trae\lizigao-box
git init
git add .
git commit -m "feat: 初始化项目"
# GitHub 新建空 repo: lizigao-box (private 也行)
git remote add origin https://github.com/你的用户名/lizigao-box.git
git branch -M main
git push -u origin main
```

### 1.2 Cloudflare Pages 部署 🤚 你操作

1. 打开 https://dash.cloudflare.com → Pages
2. **Create a project** → **Connect to Git** → 选 `lizigao-box` 仓库
3. **Build settings**：
   - Build command: `npm run build`
   - Build output: `dist`
   - Root directory: (留空)
4. **Environment variables**（暂留空）→ Save and Deploy
5. 2-3 分钟后拿到 `https://lizigao-box.pages.dev`

### 1.3 验证 🤖 我做

- ✅ 首页能打开
- ✅ 3 套主题切换正常
- ✅ `/data` 页面有指数快照
- ✅ `/downloads` 页面有下载卡片
- ✅ `/projects/excel-auto-tool/` 等详情页能打开
- ✅ OG 图、favicon、PWA manifest 都正常加载

---

## 阶段 2：注入配置（让功能活起来）

### 2.1 Plausible 域名 🤚 你操作

1. 注册 [plausible.io](https://plausible.io)（试用 30 天，付费 $9/月）
2. 注册时填的域名 = `lizigao-box.pages.dev`
3. **把域名告诉我** → 我填到 [src/consts.ts#L63](src/consts.ts#L63) 的 `PLAUSIBLE_DOMAIN`
4. 推送 → 自动部署 → 验证 Plausible 后台有访问数据

### 2.2 Cloudflare API Token 🤚 你操作

1. Cloudflare → My Profile → API Tokens → Create Token
2. 选 **Edit Cloudflare Pages** 模板
3. **Apply to specific resources** 选 `lizigao-box` 项目
4. 创建后**把 Token 复制给我**（只显示一次！）
5. 我会注入到：
   - **Cloudflare Pages Environment variables**（每次构建用）
     - `CLOUDFLARE_API_TOKEN`
     - `CLOUDFLARE_ACCOUNT_ID`（顺便从 dash 拿）
   - **GitHub repo Secrets → Actions**（GitHub Actions 自动部署用）
     - `CLOUDFLARE_API_TOKEN`
     - `CLOUDFLARE_ACCOUNT_ID`
6. 之后 `git push` → 自动构建 + 自动部署

### 2.3 Giscus 评论 🤚 你操作

1. 在 GitHub 仓库开启 **Discussions**（Settings → General → Features → ✅ Discussions）
2. 在 Discussions 创建分类 `Announcements`
3. 打开 https://giscus.app/zh-CN 填好：
   - 仓库：`你的用户名/lizigao-box`
   - 分类：`Announcements`
   - 页面 ↔ discussion 映射：`specific term`
4. 复制生成的 **repo ID** 和 **category ID** 给我
5. 我填到 [src/consts.ts#L47-L56](src/consts.ts#L47-L56) 的 `GISCUS` 常量
6. 推送 → 验证每个项目详情页底部出现评论区

---

## 阶段 3：EXE 应用上线（应用发布后再做）

### 3.1 上传 EXE 文件 🤚 你操作

把以下文件放到 `public/downloads/`：

```
public/downloads/
  ├── ExcelAutoTool-Setup-1.0.0.exe
  ├── ExcelAutoTool-Setup-1.0.0.exe.sha256    ← 校验和文件
  ├── ArtistTool-1.0.0-portable.exe
  ├── ArtistTool-1.0.0-portable.exe.sha256
  ├── MultiAgentHub-Setup-0.5.0.exe
  └── MultiAgentHub-Setup-0.5.0.exe.sha256
```

### 3.2 算 SHA256 🤚 你操作

```powershell
# 在 lizigao-box 目录下
Get-FileHash "public\downloads\ExcelAutoTool-Setup-1.0.0.exe" -Algorithm SHA256
```

把 3 个 EXE 的 SHA256 值都给我。

### 3.3 更新元数据 🤖 我做

我更新 [src/lib/downloads.ts](src/lib/downloads.ts)：
- 替换 `PLACEHOLDER_REPLACE_AFTER_BUILD` 为真实 SHA256
- 更新 `size` 为真实文件字节数
- 更新 `releasedAt` 为发布日

### 3.4 下载计数后端（可选）🤚 你操作

注册 [upstash.com](https://upstash.com)（免费 10K 请求/天）：
1. Create Database → 选 Global 区域 → 命名 `lizigao-downloads`
2. 复制 **REST URL** 和 **REST Token** 给我
3. 我加到 Cloudflare Environment variables：
   - `UPSTASH_REDIS_REST_URL`
   - `UPSTASH_REDIS_REST_TOKEN`
4. **不配也能用**，只是下载计数永远是 0

---

## 阶段 4：上线后维护（持续）

### 自动化已就位 ✅
- ✅ 每日 16:00 北京时间自动抓取指数快照
- ✅ `git push` 自动部署到 Cloudflare Pages
- ✅ PR 自动验证构建（build-verify.yml）
- ✅ Plausible 自动统计访问
- ✅ Plausible 自动追踪下载、点击事件

### 你要做的 🤚
- 收到 PR 邮件 → 看 build 是否过
- 定期看 Plausible 数据
- 用户提 issue → 修

---

## 🎯 你现在最该做的（按优先级）

| 优先级 | 任务 | 时间 | 你需要的 |
|--------|------|------|----------|
| 🔴 P0 | 推 GitHub（1.1） | 5min | GitHub 账号 |
| 🔴 P0 | Cloudflare 部署（1.2） | 5min | Cloudflare 账号 |
| 🟡 P1 | Plausible 域名（2.1） | 3min | plausible.io 注册 |
| 🟡 P1 | CF API Token（2.2） | 3min | Cloudflare 后台 |
| 🟢 P2 | Giscus 启用（2.3） | 10min | GitHub Discussions 开启 |
| 🟢 P3 | EXE 上线（3.x） | 应用发布后再说 | EXE 文件 |

**最快的路径：先做完 P0，让站跑起来。然后慢慢补 P1/P2。**

---

## ❓ 我现在能直接做的（不需要你操作）

- [x] ~~OG Image 自动生成~~ ✅
- [x] ~~Plausible 集成（等域名）~~ ✅
- [x] ~~CF Actions 自动部署（等 Token）~~ ✅
- [x] ~~favicon + logo 双主题~~ ✅
- [x] ~~Giscus 评论组件 + 配置开关~~ ✅
- [x] ~~下载中心 + 计数系统~~ ✅
- [x] ~~主页下载入口~~ ✅
- [x] ~~应用统一 Windows 平台~~ ✅
- [x] ~~项目页评论集成~~ ✅
- [x] ~~PR 构建验证 workflow~~ ✅
- [x] ~~PWA manifest~~ ✅
- [ ] **等你给值后**：填 Plausible 域名、CF Token、Giscus ID
- [ ] **应用发布后**：填 SHA256 + 文件大小
