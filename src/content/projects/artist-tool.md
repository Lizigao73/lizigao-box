---
title: ArtistTool 画手工具箱
status: building
category: desktop
summary: 给画手用的桌面工具合集：截图标注 / 速写日历 / 素材管理 / 速写训练。
tags: [electron, vue, desktop, creative]
startDate: 2026-05-15
links:
  - type: article
    label: 需求文档 PRD
    url: https://github.com/lizigao-box/notes
featured: true
order: 2
---

## 起因

画手朋友提了几次需求：截图标注、速写训练计划、参考图管理……市面上的工具都是分散的，一个屏幕标注、一个日历、一个文件管理器，切换成本高。

**ArtistTool** 想做的是一个"画手桌面"，把日常创作需要的小工具集成在同一个壳里。

## 模块

- **ScreenSnap**：截图 + 区域标注 + 颜色取样
- **SketchCalendar**：速写日历，每日打卡、统计连续天数
- **SketchTrainer**：参考图训练，随机出题 / 限时模式
- **FileManager**：本地素材库，标签 + 缩略图

## 状态

- [x] ScreenSnap 区域截图
- [x] SketchCalendar 日历视图
- [ ] SketchTrainer（原型）
- [ ] FileManager（设计阶段）

## 设计取向

界面追求**安静、克制、专注**——深色调、小尺寸按钮、圆角柔和、装饰元素最小化。速写日历是核心模块，给用户"完成感"是首要目标——一个绿色勾比一段鼓励文字有效得多。
