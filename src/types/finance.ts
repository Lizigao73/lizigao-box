// 金融快照数据类型
export interface FinancialSnapshot {
  /** 日期 YYYY-MM-DD */
  date: string;
  /** 上证指数 */
  shIndex: number | null;
  /** 深证成指 */
  szIndex: number | null;
  /** 标普 500 */
  sp500: number | null;
  /** 纳斯达克 */
  nasdaq: number | null;
  /** 抓取时间 ISO */
  fetchedAt: string;
}

export interface FinancialData {
  lastUpdated: string;
  source: string;
  snapshots: FinancialSnapshot[];
}

export interface IndexWithChange {
  name: string;
  code: string;
  value: number | null;
  /** 与上一日相比的绝对变化 */
  change: number | null;
  /** 变化百分比（0.0123 = 1.23%） */
  changePct: number | null;
}
