---
title: 指数快照 · 在线追踪
status: online
category: data
summary: 每天收盘后自动抓取 A 股 / 美股主要指数的快照，存为 JSON 并展示在本站 /data 页面。
tags: [data, finance, github-actions, automation]
startDate: 2026-05-01
links:
  - type: github
    label: 数据抓取脚本
    url: https://github.com/lizigao-box/fetch-snapshots
  - type: external
    label: 查看数据
    url: /data
order: 4
---

## 关于这个项目

> 站内的 `/data` 页面就是这个项目的展示。**零成本**的数据看板。

## 架构

```
GitHub Actions (每日 16:00 北京时间)
  ↓ 跑 Python 脚本
抓取 akshare / yfinance 数据
  ↓ 写入
src/data/financial-snapshots.json
  ↓ git commit + push
触发 Vercel 自动部署
  ↓ 构建时读取 JSON
/data 页面渲染当日快照 + 30 日折线
```

## 抓取的指数

- **上证指数** (sh000001)
- **深证成指** (sz399001)
- **标普 500** (^SPX)
- **纳斯达克** (^IXIC)

## 为什么做这个

- 练习 GitHub Actions 定时任务
- 体验"全静态 + 定时数据"这种轻量架构
- 给自己一个日常看的小看板
- 顺便测试不同图表库（ECharts / Chart.js）的效果

## 后续

- [ ] 加更多指数（创业板、恒生、比特币）
- [ ] 加"涨跌幅热力图"
- [ ] 周报自动生成（让 Actions 写 Markdown）
