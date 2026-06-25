// src/lib/downloads.ts
// 下载元数据 + 计数管理（用 Vercel KV）

export interface DownloadEntry {
  /** 下载 ID（URL 里用） */
  id: string;
  /** 显示名 */
  name: string;
  /** 简短描述 */
  description: string;
  /** 文件名（含版本） */
  filename: string;
  /** 文件大小（字节） */
  size: number;
  /** SHA256 校验和（hex） */
  sha256: string;
  /** 版本 */
  version: string;
  /** 平台：当前仅 Windows */
  platform: 'windows';
  /** 发布时间 ISO */
  releasedAt: string;
  /** 存储路径（Vercel Blob / S3 / 本地 public） */
  storage: 'blob' | 'public';
  /** Blob URL（storage='blob' 时使用） */
  blobUrl?: string;
}

// EXE 注册表
export const DOWNLOADS: DownloadEntry[] = [
  {
    id: 'excel-auto-tool-windows',
    name: 'Excel 自动化工具 · Windows',
    description: '可视化流程编辑器 · Windows 10/11 64-bit 安装包',
    filename: 'ExcelAutoTool-Setup-1.0.0.exe',
    size: 45_200_000, // ~45 MB
    sha256: 'PLACEHOLDER_REPLACE_AFTER_BUILD',
    version: '1.0.0',
    platform: 'windows',
    releasedAt: '2026-06-15T00:00:00Z',
    storage: 'public',
  },
  {
    id: 'artist-tool-windows',
    name: '画手工具箱 · Windows',
    description: '截图标注 / 速写日历 / 素材管理 · 绿色版',
    filename: 'ArtistTool-1.0.0-portable.exe',
    size: 28_700_000,
    sha256: 'PLACEHOLDER_REPLACE_AFTER_BUILD',
    version: '1.0.0',
    platform: 'windows',
    releasedAt: '2026-06-10T00:00:00Z',
    storage: 'public',
  },
  {
    id: 'multi-agent-hub-windows',
    name: '智能体协作中心 · Windows',
    description: '多 LLM 智能体分工 · 安装版',
    filename: 'MultiAgentHub-Setup-0.5.0.exe',
    size: 62_300_000,
    sha256: 'PLACEHOLDER_REPLACE_AFTER_BUILD',
    version: '0.5.0-beta',
    platform: 'windows',
    releasedAt: '2026-06-20T00:00:00Z',
    storage: 'public',
  },
];

export function findDownload(id: string): DownloadEntry | undefined {
  return DOWNLOADS.find(d => d.id === id);
}

export function formatSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  if (bytes < 1024 * 1024 * 1024) return `${(bytes / 1024 / 1024).toFixed(1)} MB`;
  return `${(bytes / 1024 / 1024 / 1024).toFixed(2)} GB`;
}
