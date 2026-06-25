# 下载文件目录

把编译好的 EXE / DMG / AppImage 放到这里，**文件名必须与 `src/lib/downloads.ts` 里的 `filename` 一致**。

## 当前文件

- `ExcelAutoTool-Setup-1.0.0.exe` (45 MB) — Excel 自动化工具 Windows 安装包
- `ArtistTool-1.0.0-portable.exe` (28 MB) — 画手工具箱绿色版
- `MultiAgentHub-Setup-0.5.0.exe` (62 MB) — 智能体协作中心安装包

## 计算 SHA256

```powershell
Get-FileHash .\ExcelAutoTool-Setup-1.0.0.exe -Algorithm SHA256
```

把 hash 填到 `src/lib/downloads.ts` 的 `sha256` 字段。

## 大文件用 Vercel Blob

> ⚠️ GitHub 单文件 100MB 限制，Vercel Hobby 部署 250MB 限制。

如果 EXE 超过 100MB：
1. 上传到 Vercel Blob：`vercel blob put ExcelAutoTool-Setup-1.0.0.exe`
2. 把 `storage: 'blob'` + `blobUrl: 'https://xxx.public.blob.vercel-storage.com/...'`
3. 部署后访问 `/downloads` 看效果
