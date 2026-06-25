"""
fetch_snapshots.py - 抓取 A 股 / 美股主要指数收盘数据

数据源：
  - A 股：akshare（stock_zh_index_daily）
  - 美股：yfinance（^SPX, ^IXIC）
输出：src/data/financial-snapshots.json
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "src" / "data" / "financial-snapshots.json"

BJ_TZ = timezone(timedelta(hours=8))


def _today_bj() -> str:
    return datetime.now(BJ_TZ).strftime("%Y-%m-%d")


def _now_bj_iso() -> str:
    return datetime.now(BJ_TZ).isoformat(timespec="seconds")


def fetch_a_share(symbol: str) -> float | None:
    """抓 A 股指数（akshare）"""
    try:
        import akshare as ak
    except ImportError:
        print("akshare 未安装", file=sys.stderr)
        return None
    try:
        df = ak.stock_zh_index_daily(symbol=symbol)
        if df is None or df.empty:
            return None
        return float(df["close"].iloc[-1])
    except Exception as e:
        print(f"akshare 获取 {symbol} 失败：{e}", file=sys.stderr)
        return None


def fetch_us_index(symbol: str) -> float | None:
    """抓美股指数（yfinance）"""
    try:
        import yfinance as yf
    except ImportError:
        print("yfinance 未安装", file=sys.stderr)
        return None
    try:
        t = yf.Ticker(symbol)
        hist = t.history(period="5d")
        if hist is None or hist.empty:
            return None
        return float(hist["Close"].iloc[-1])
    except Exception as e:
        print(f"yfinance 获取 {symbol} 失败：{e}", file=sys.stderr)
        return None


def main() -> int:
    today = _today_bj()
    now_iso = _now_bj_iso()

    sh  = fetch_a_share("sh000001")
    sz  = fetch_a_share("sz399001")
    sp  = fetch_us_index("^SPX")
    nas = fetch_us_index("^IXIC")

    # 读已有数据
    if OUT.exists():
        data = json.loads(OUT.read_text(encoding="utf-8"))
    else:
        data = {"lastUpdated": now_iso, "source": "akshare + yfinance", "snapshots": []}

    snapshots = data.get("snapshots", [])

    # 找到今日（不存在）或昨日（最后一条）以便去重
    existing_idx = next(
        (i for i, s in enumerate(snapshots) if s.get("date") == today),
        None,
    )
    new_entry = {
        "date": today,
        "shIndex": sh,
        "szIndex": sz,
        "sp500": sp,
        "nasdaq": nas,
        "fetchedAt": now_iso,
    }
    if existing_idx is not None:
        snapshots[existing_idx] = new_entry
    else:
        snapshots.append(new_entry)

    # 限制最多保留 365 天
    snapshots = snapshots[-365:]

    data["lastUpdated"] = now_iso
    data["source"] = "akshare + yfinance (GitHub Actions 定时抓取)"
    data["snapshots"] = snapshots

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"✓ 已写入 {OUT}：{len(snapshots)} 条快照")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
