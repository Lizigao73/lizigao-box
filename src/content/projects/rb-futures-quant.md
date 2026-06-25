---
title: 螺纹钢期货 · 量化策略
status: shipped
category: data
summary: 基于 VNPY 框架的螺纹钢趋势跟踪策略，含回测 / 优化 / 部署全套脚本。
tags: [python, vnpy, quant, futures, rb]
startDate: 2025-08-16
links:
  - type: article
    label: 策略说明
    url: https://github.com/lizigao-box/notes
  - type: external
    label: 回测报告
    url: https://github.com/lizigao-box/notes/rb-report
featured: true
order: 3
---

## 项目概览

这是最早做的"完整的"量化项目——从数据收集、回测、参数优化、稳定性测试到部署脚本全部跑通。策略本身不复杂，**核心是把工程链路走通**。

## 策略逻辑

- **标的**：螺纹钢主力合约 (RB)
- **周期**：日线
- **信号**：双均线 + ATR 波动率过滤
- **风控**：单笔风险 1%，最大持仓 2 手

## 工程产出

```
data/                 # 历史数据
strategies/           # 策略代码
deploy/               # 部署脚本
results/              # 回测结果、参数优化记录
monitor/              # 实时监控 + 项目状态
```

## 回测结果（2020–2024）

| 指标 | 数值 |
|------|------|
| 年化收益 | 18.2% |
| 最大回撤 | -7.8% |
| 胜率 | 52.3% |
| 盈亏比 | 1.86 |
| 夏普 | 1.42 |

> 数字仅供参考，未考虑手续费、滑点和真实交易摩擦。

## 教训

- **回测 ≠ 实盘**：过拟合是第一大坑，参数稳定区间比绝对收益更重要
- **数据质量**：拿到数据后先花一周清洗，比写策略的时间还长
- **工程化**：从一开始就把数据、策略、回测分离，否则后面重构要命
