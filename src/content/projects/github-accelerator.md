---
title: GitHub 加速器
status: shipped
category: desktop
summary: 通过修改系统 Hosts 文件，智能测速选 IP，加速 GitHub 及常见开发站点访问。
tags: [python, tkinter, desktop, network]
startDate: 2026-06-26
links:
  - type: download
    label: 下载 v2.1
    url: /downloads#github-accelerator-windows
featured: true
order: 2
---

## 起因

国内访问 GitHub、GitLab、Docker Hub、Hugging Face 等开发站点时，经常遇到 DNS 污染或 IP 被阻断的问题。手动改 hosts 文件太繁琐，每次都要查 IP、编辑、刷新 DNS。

**GitHub 加速器** 想做的就是把这件事一键化——可视化勾选要加速的站点，自动测速选最快的 IP，写入 hosts，刷新 DNS。

## 做了什么

- **智能测速**：更新 IP 前 TCP 测速，自动选延迟最低的 5 个 IP 写入 Hosts
- **多站点组**：GitHub、GitLab、Docker Hub、Hugging Face、PyPI 等 7 组，每组内子站点独立勾选
- **一键启用 / 恢复**：写入前自动备份原始 hosts，支持一键恢复
- **12h 后台自动刷新**：静默线程每 12h 拉取测速更新 IP，日志提示
- **用户偏好持久化**：勾选状态、展开状态、窗口位置保存到本地，下次打开恢复
- **管理员权限自动提升**：检测并以管理员权限重新启动

## 技术栈

```
语言：Python 3.11
GUI：tkinter + ttk（自定义 ModernScrollbar 圆角滚动条）
打包：PyInstaller 6.21.0（onedir 模式）
配置：sites.json（可扩展）
配色：深色主题 (#1a1b1d 背景 + 莫兰迪淡青主调)
```

## 当前进度

- [x] 多站点组勾选
- [x] 智能测速选 IP
- [x] 一键写入 / 恢复 hosts
- [x] 自动管理员权限提升
- [x] 用户偏好持久化
- [x] 12h 后台自动刷新
- [x] 自定义圆角滚动条
- [x] 日志面板（复制 / 清空）
- [x] 打包成 zip 分发（10.3 MB）

## 一些有意思的细节

> 测速用 TCP connect 测延迟，不依赖 HTTP，更快更稳。选最快的 5 个 IP 写入 hosts，避免单 IP 失效时全挂。

> 深色主题滚动条用 Canvas 自绘制圆角长条，悬停时滑块高亮变色，比 ttk 原生样式更现代。

站内有专文讲实现，持续更新。