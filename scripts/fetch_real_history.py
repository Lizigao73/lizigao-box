"""
fetch_real_history.py - 抓取近 30 日真实历史数据

数据源：
  - A 股：新浪财经（sh000001, sz399001）
  - 美股：腾讯财经（us.INX = 标普 500, us.IXIC = 纳斯达克）
输出：src/data/financial-snapshots.json
"""

from __future__ import annotations

import json
import re
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "src" / "data" / "financial-snapshots.json"

BJ_TZ = timezone(timedelta(hours=8))


def _today_bj() -> str:
    return datetime.now(BJ_TZ).strftime("%Y-%m-%d")


def _now_bj_iso() -> str:
    return datetime.now(BJ_TZ).isoformat(timespec="seconds")


def _http_get(url: str, headers: dict | None = None, timeout: int = 15) -> bytes:
    req = Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        **(headers or {}),
    })
    with urlopen(req, timeout=timeout) as resp:
        return resp.read()


# ============== A 股：新浪 ==============

def fetch_sina_cn(symbol: str, days: int = 35) -> list[tuple[str, float]]:
    """新浪 A 股 kline。symbol 形如 sh000001 / sz399001"""
    url = (
        f"https://money.finance.sina.com.cn/quotes_service/api/json_v2.php"
        f"/CN_MarketData.getKLineData?symbol={symbol}&scale=240&ma=no&datalen={days}"
    )
    try:
        text = _http_get(url, timeout=15).decode("utf-8", errors="replace")
    except (HTTPError, URLError) as e:
        print(f"  sina {symbol} 失败: {e}", file=sys.stderr)
        return []
    try:
        arr = json.loads(text)
    except json.JSONDecodeError:
        print(f"  sina {symbol} 解析失败", file=sys.stderr)
        return []
    out = []
    for item in arr:
        d = item.get("day")
        c = item.get("close")
        if d and c:
            try:
                out.append((d, float(c)))
            except ValueError:
                continue
    out.sort(key=lambda x: x[0])
    return out


# ============== 美股：腾讯 ==============

def fetch_tx_us(symbol: str, days: int = 35) -> list[tuple[str, float]]:
    """腾讯美股 kline。symbol 形如 us.INX / us.IXIC / us.DJI"""
    url = (
        f"https://web.ifzq.gtimg.cn/appstock/app/fqkline/get"
        f"?_var=kline_dayqf&param={symbol},day,,,{days},qfq"
    )
    try:
        text = _http_get(url, timeout=15).decode("utf-8", errors="replace")
    except (HTTPError, URLError) as e:
        print(f"  tx {symbol} 失败: {e}", file=sys.stderr)
        return []
    # 形如 kline_dayqf={"code":0,"msg":"","data":{"us.IXIC":{"day":[[date,open,close,high,low,vol], ...]}, ...}}
    try:
        m = re.search(r'=\s*(\{.*\})\s*$', text)
        if not m:
            print(f"  tx {symbol} 格式异常", file=sys.stderr)
            return []
        data = json.loads(m.group(1))
        sym_data = (data.get("data") or {}).get(symbol) or {}
        days_arr = sym_data.get("day") or []
        out = []
        for row in days_arr:
            # [date, open, close, high, low, volume]
            if len(row) < 3 or row[0] is None or row[2] is None:
                continue
            try:
                out.append((row[0], float(row[2])))
            except (ValueError, TypeError):
                continue
        out.sort(key=lambda x: x[0])
        return out
    except (json.JSONDecodeError, KeyError) as e:
        print(f"  tx {symbol} 解析失败: {e}", file=sys.stderr)
        return []


# ============== main ==============

def main() -> int:
    now_iso = _now_bj_iso()

    print("=== 抓取近 30 日真实数据 ===")
    # 并行拉 4 路
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=4) as pool:
        f_sp  = pool.submit(fetch_tx_us,   "us.INX",  35)
        f_nas = pool.submit(fetch_tx_us,   "us.IXIC", 35)
        f_sh  = pool.submit(fetch_sina_cn, "sh000001", 35)
        f_sz  = pool.submit(fetch_sina_cn, "sz399001", 35)
        sp, nas, sh, sz = f_sp.result(), f_nas.result(), f_sh.result(), f_sz.result()
    print(f"  -> 标普 {len(sp)} / 纳指 {len(nas)} / 上证 {len(sh)} / 深证 {len(sz)}")

    if not any([sp, nas, sh, sz]):
        print("\n全部抓取失败，保持原数据", file=sys.stderr)
        return 1

    all_dates = sorted({d for d, _ in sp} | {d for d, _ in nas} |
                       {d for d, _ in sh} | {d for d, _ in sz})
    # 限制最多 30 天
    all_dates = all_dates[-30:]

    # 字典化（O(1) 查找）替代原 O(n) 线性扫描
    sh_map  = dict(sh)
    sz_map  = dict(sz)
    sp_map  = dict(sp)
    nas_map = dict(nas)

    snapshots = []
    for d in all_dates:
        entry = {
            "date": d,
            "shIndex": sh_map.get(d),
            "szIndex": sz_map.get(d),
            "sp500":   sp_map.get(d),
            "nasdaq":  nas_map.get(d),
            "fetchedAt": now_iso,
        }
        if any(v is not None for v in [entry["shIndex"], entry["szIndex"], entry["sp500"], entry["nasdaq"]]):
            snapshots.append(entry)

    if not snapshots:
        print("无有效数据，保持原文件", file=sys.stderr)
        return 1

    # 填补 None（forward fill）
    for key in ["shIndex", "szIndex", "sp500", "nasdaq"]:
        last = None
        for s in snapshots:
            if s[key] is None:
                s[key] = last
            else:
                last = s[key]

    data = {
        "lastUpdated": now_iso,
        "source": "新浪财经 (sh000001, sz399001) · 腾讯财经 (us.INX, us.IXIC)",
        "note": f"近 {len(snapshots)} 个交易日真实历史收盘价。",
        "snapshots": snapshots,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"\n✓ 已写入 {OUT}")
    print(f"  {len(snapshots)} 条快照（{snapshots[0]['date']} → {snapshots[-1]['date']}）")
    for k, label in [("shIndex", "上证"), ("szIndex", "深证"), ("sp500", "标普"), ("nasdaq", "纳指")]:
        v = snapshots[-1].get(k)
        print(f"  {label} 最新: {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
