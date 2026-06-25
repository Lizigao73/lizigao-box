---
title: ExcelAutoTool
status: building
category: desktop
summary: 可视化流程编辑器 + Python 执行后端，把重复 Excel 操作拖拽成自动化流水线。
tags: [electron, vue, python, excel, desktop]
startDate: 2026-04-01
links:
  - type: article
    label: 设计与实现笔记
    url: https://github.com/lizigao-box/notes
featured: true
order: 1
---

## 起因

日常做表格的同事经常需要重复执行一连串操作：清洗列、合并文件、按规则拆分、生成报表。这些操作每次都写 Python 脚本太重，每次手动点又太慢。

**ExcelAutoTool** 想做的就是在中间找个平衡点——把"步骤"拖到画布上连成流水线，让非程序员也能复用。

## 做了什么

- **可视化画布**：左侧组件库 + 中间画布 + 右侧参数面板，三栏布局
- **节点系统**：支持读取、清洗、转换、输出四大类节点，可自定义字段
- **执行后端**：Python + pandas/openpyxl，由 Electron IPC 调度
- **流程保存/加载**：JSON 序列化到本地，支持工作流批量执行
- **Ctrl+Z**：30 步历史，撤销/重做
- **多 Tab 画布**：同时编辑多个流程

## 技术栈

```
前端：Electron + Vue 3 + Pinia
后端：Python 3.10 + pandas + openpyxl
通信：IPC (contextBridge)
打包：electron-builder
```

## 当前进度

- [x] 节点拖拽 / 连线 / 删除
- [x] 流程保存/加载
- [x] 多 Tab 编辑
- [x] Ctrl+Z 撤销（30 步）
- [x] 字段预测（拓扑排序）
- [ ] 工作流调度
- [ ] 远程执行（云端沙箱）
- [ ] 节点市场（用户自定义节点）

## 一些有意思的细节

> 字段预测用拓扑排序 + BFS，根据节点类型和上下游连接关系，递归推算每个节点的输出字段。这样用户加一个新节点时，立刻能看到"它会产生哪些字段"，不必等真正执行。

站内有专文讲实现，GitHub 仓库持续更新。
