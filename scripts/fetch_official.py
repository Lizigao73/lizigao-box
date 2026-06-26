"""
fetch_official.py - 严肃整顿后的官方数据源抓取脚本

数据源（全部为官方/权威渠道）：
  - A 股 (sh000001, sz399001):
      akshare.stock_zh_index_daily → 新浪财经
  - 标普 500 (.INX) / 纳斯达克综合 (.IXIC):
      akshare.index_us_stock_sina → 新浪财经美股指数
  - 伦敦黄金 (XAU):
      akshare.futures_foreign_hist → 新浪外盘期货
  - 美元指数 (DXY):
      新浪 hq DINI 实时报价（历史通过最近若干个交易日采样）

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
SINA_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "Accept": "*/*",
    "Referer": "https://finance.sina.com.cn/",
}


def _today_bj() -> str:
    return datetime.now(BJ_TZ).strftime("%Y-%m-%d")


def _now_bj_iso() -> str:
    return datetime.now(BJ_TZ).isoformat(timespec="seconds")


def _http_get(url: str, headers: dict | None = None, timeout: int = 20) -> bytes:
    h = {**SINA_HEADERS, **(headers or {})}
    req = Request(url, headers=h)
    with urlopen(req, timeout=timeout) as r:
        return r.read()


def _http_get_with_retry(url: str, attempts: int = 3, timeout: int = 20) -> bytes | None:
    """带退避重试的 GET，单次失败不抛出"""
    last_err = ""
    for i in range(attempts):
        try:
            return _http_get(url, timeout=timeout)
        except (HTTPError, URLError, OSError, ConnectionError) as e:
            last_err = f"{type(e).__name__}: {str(e)[:80]}"
            wait = 1.5 * (i + 1)
            time.sleep(wait)
    return None


# ============== A 股：akshare → 新浪 ==============

def fetch_a_share_history(symbol: str, days: int = 250) -> list[tuple[str, float]]:
    """akshare.stock_zh_index_daily → 新浪 K 线

    返回 [(date_str, close), ...] 按日期升序
    """
    try:
        import akshare as ak
    except ImportError:
        print("  [ERR] akshare 未安装", file=sys.stderr)
        return []
    for attempt in range(3):
        try:
            df = ak.stock_zh_index_daily(symbol=symbol)
            if df is None or df.empty:
                return []
            df = df.tail(days)
            out = [(str(r['date'])[:10], float(r['close'])) for _, r in df.iterrows()]
            return out
        except Exception as e:
            print(f"  sina {symbol} 第 {attempt+1} 次失败: {e}", file=sys.stderr)
            time.sleep(1 + attempt * 2)
    return []


# ============== 美股指数：akshare.index_us_stock_sina ==============

def fetch_us_index_sina(symbol: str, days: int = 250) -> list[tuple[str, float]]:
    """akshare.index_us_stock_sina → 新浪美股指数

    symbol: .INX (标普 500), .IXIC (纳斯达克综合), .DJI (道琼斯), .NDX (纳指 100)
    """
    try:
        import akshare as ak
    except ImportError:
        return []
    for attempt in range(3):
        try:
            df = ak.index_us_stock_sina(symbol=symbol)
            if df is None or df.empty:
                return []
            df = df.tail(days)
            out = [(str(r['date'])[:10], float(r['close'])) for _, r in df.iterrows()]
            return out
        except Exception as e:
            print(f"  sina us {symbol} 第 {attempt+1} 次失败: {e}", file=sys.stderr)
            time.sleep(1 + attempt * 2)
    return []


# ============== 海外期货：akshare.futures_foreign_hist ==============

def fetch_foreign_futures(symbol: str, days: int = 250) -> list[tuple[str, float]]:
    """akshare.futures_foreign_hist → 新浪外盘期货历史

    symbol: GC (COMEX 黄金), XAU (伦敦金), ES (E-mini 标普), NQ (E-mini 纳指)
    返回列：date, open, high, low, close, volume
    """
    try:
        import akshare as ak
    except ImportError:
        return []
    for attempt in range(3):
        try:
            df = ak.futures_foreign_hist(symbol=symbol)
            if df is None or df.empty:
                return []
            df = df.tail(days)
            # df 列: 时间(date), 开盘(open), 最高(high), 最低(low), 收盘(close), ...
            # 索引可能是 0=date, 1=open, 4=close
            out = []
            date_col = df.columns[0]
            close_col = df.columns[4] if df.shape[1] > 4 else df.columns[-1]
            for _, r in df.iterrows():
                d = r[date_col]
                d_str = d.strftime("%Y-%m-%d") if hasattr(d, "strftime") else str(d)[:10]
                out.append((d_str, float(r[close_col])))
            return out
        except Exception as e:
            print(f"  foreign fut {symbol} 第 {attempt+1} 次失败: {e}", file=sys.stderr)
            time.sleep(1 + attempt * 2)
    return []


# ============== 美元指数（DXY）兜底：sina hq DINI ==============

def fetch_dxy_realtime() -> float | None:
    """sina hq DINI 实时报价（仅拿当日值）"""
    raw = _http_get_with_retry("https://hq.sinajs.cn/list=DINI", timeout=10)
    if raw is None:
        return None
    try:
        text = raw.decode("gbk", errors="replace")
        m = re.search(r'"([^"]+)"', text)
        if not m:
            return None
        parts = m.group(1).split(",")
        # DINI 字段: 时间, 当前价, 最高, 最低, 昨收, ... （具体看接口）
        if len(parts) >= 2:
            try:
                # 字段 1 是最新价（部分品种），字段 5 是昨收
                # 实际接口返回是 02:49:27 101.3428 101.3428 101.4559 5267 101.4599 ...
                # 索引 1 = 当前价, 索引 5 = 昨收
                cur = float(parts[1]) if parts[1] else None
                if cur is not None and 80 < cur < 130:
                    return cur
            except (ValueError, IndexError):
                pass
        return None
    except Exception as e:
        print(f"  DXY 解析失败: {e}", file=sys.stderr)
        return None


# ============== main ==============

def main() -> int:
    now_iso = _now_bj_iso()
    today = _today_bj()

    print("=== 抓取真实数据（akshare 新浪源）===")
    print("数据源（全部为官方/权威渠道）：")
    print("  - A 股 (sh000001, sz399001)            : akshare.stock_zh_index_daily")
    print("  - 标普 500 (.INX) / 纳指 (.IXIC)       : akshare.index_us_stock_sina")
    print("  - 伦敦金 (XAU) / 黄金 (GC)             : akshare.futures_foreign_hist")
    print("  - 美元指数 (DXY)                        : sina hq DINI（实时）")
    print()

    # akshare 内部使用 mini_racer 跑 JS，多线程不稳定 → 串行调用
    print("  [1/6] 上证指数 ...")
    sh_hist = fetch_a_share_history("sh000001", 250)
    print(f"        -> {len(sh_hist)} 条")
    print("  [2/6] 深证成指 ...")
    sz_hist = fetch_a_share_history("sz399001", 250)
    print(f"        -> {len(sz_hist)} 条")
    print("  [3/6] 标普 500 ...")
    sp_hist = fetch_us_index_sina(".INX", 250)
    print(f"        -> {len(sp_hist)} 条")
    print("  [4/6] 纳斯达克综合 ...")
    nas_hist = fetch_us_index_sina(".IXIC", 250)
    print(f"        -> {len(nas_hist)} 条")
    print("  [5/6] 伦敦金 XAU ...")
    xau_hist = fetch_foreign_futures("XAU", 250)
    print(f"        -> {len(xau_hist)} 条")
    if not xau_hist:
        print("  [5b/6] COMEX 黄金 GC (fallback) ...")
        gld_hist = fetch_foreign_futures("GC", 250)
        print(f"         -> {len(gld_hist)} 条")
    else:
        gld_hist = []
    # DXY 用线程池独立抓（不涉及 mini_racer）
    print("  [6/6] 美元指数 DXY (sina hq DINI) ...")
    dxy_now = fetch_dxy_realtime()
    print(f"        -> {dxy_now}")

    print(f"\n  上证 {len(sh_hist)} 条 | 深证 {len(sz_hist)} 条")
    print(f"  标普 {len(sp_hist)} 条 | 纳指 {len(nas_hist)} 条")
    print(f"  伦敦金 {len(xau_hist)} 条 | COMEX 黄金 {len(gld_hist)} 条")
    print(f"  美元指数实时价: {dxy_now}")

    success_count = sum(1 for h in (sh_hist, sz_hist, sp_hist, nas_hist) if h)
    if success_count < 2:
        print("\n可用数据源少于 2 个，放弃写入", file=sys.stderr)
        return 1

    # 黄金取 XAU（伦敦金）优先
    gold_hist = xau_hist if xau_hist else gld_hist
    gold_source = "伦敦金 (XAU)" if xau_hist else "COMEX 黄金 (GC)"

    # 字典化（O(1) 查找）
    sh_map  = {d: v for d, v in sh_hist}
    sz_map  = {d: v for d, v in sz_hist}
    sp_map  = {d: v for d, v in sp_hist}
    nas_map = {d: v for d, v in nas_hist}
    gld_map = {d: v for d, v in gold_hist}
    # DXY 没有 K 线，先用 None（前端会显示 N/A）
    dxy_map: dict[str, float] = {}

    # 全部日期（取并集，按升序）
    all_dates = sorted(
        set(sh_map) | set(sz_map) | set(sp_map) | set(nas_map) | set(gld_map) | set(dxy_map)
    )
    if not all_dates:
        print("无日期数据", file=sys.stderr)
        return 1

    # 构造快照
    snapshots = []
    for d in all_dates:
        snapshots.append({
            "date": d,
            "shIndex": sh_map.get(d),
            "szIndex": sz_map.get(d),
            "sp500":   sp_map.get(d),
            "nasdaq":  nas_map.get(d),
            "gold":    gld_map.get(d),
            "dxy":     dxy_map.get(d),
            "fetchedAt": now_iso,
        })

    # forward fill 缺失值（仅对有源数据的字段）
    for key in ("shIndex", "szIndex", "sp500", "nasdaq", "gold"):
        last = None
        for s in snapshots:
            if s[key] is None:
                if last is not None:
                    s[key] = last
            else:
                last = s[key]

    # 把 DXY 实时价挂到最新一条（仅当日）
    if dxy_now is not None and snapshots:
        snapshots[-1]["dxy"] = dxy_now

    # 打印最后 3 条
    print("\n=== 最近 3 个交易日 ===")
    for s in snapshots[-3:]:
        print(f"  {s['date']}  上证={s['shIndex']} 深证={s['szIndex']} 标普={s['sp500']} 纳指={s['nasdaq']} 黄金={s['gold']} DXY={s['dxy']}")

    # 写回
    data = {
        "lastUpdated": now_iso,
        "source": (
            f"A股(akshare-新浪 sh000001/sz399001) · "
            f"标普500/纳指(akshare.index_us_stock_sina .INX/.IXIC) · "
            f"{gold_source}(akshare.futures_foreign_hist) · "
            f"美元指数(sina hq DINI 实时，仅当日)"
        ),
        "snapshots": snapshots,
    }
    OUT.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"\n✓ 已写入 {OUT}：{len(snapshots)} 条（{snapshots[0]['date']} → {snapshots[-1]['date']}）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
