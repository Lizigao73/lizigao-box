---
title: 股票期货对比分析
status: shipped
category: data
summary: A 股主要指数 vs 美股主要指数的相关性、风险收益对比，附可视化报告。
tags: [python, pandas, matplotlib, finance]
startDate: 2025-09-01
links:
  - type: article
    label: 分析报告
    url: https://github.com/lizigao-box/notes
order: 6
---

## 概览

用 akshare + yfinance 拉数据，对 A 股（上证、深证）和美股（标普、纳指）做相关性、波动率、风险收益的对比分析。

## 输出

- `correlation_matrix.csv` / `*.png`
- `risk_return_metrics.csv`
- `data_analysis_summary.txt`
- 各指数价格走势图

## 主要发现

- A 股和美股的相关性显著低于美股内部相关性
- 纳指波动率最大，但长期收益也最高
- 上证波动率与纳指接近，但收益分布差异很大

## 工程要点

- 数据清洗占 60% 的工作量
- matplotlib 中文显示需要额外配字体
- 报表用纯 HTML 静态生成，无服务器
