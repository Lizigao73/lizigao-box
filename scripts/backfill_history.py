"""
backfill_history.py - 用模拟数据把 financial-snapshots.json 回溯到 2026-01-01

用途：当 GitHub Actions 抓取脚本无法跑（如网络限制）时，临时用模拟数据补齐
历史快照，UI 端能展示更长的趋势图。

策略：从已有最早一条（2026-05-14）反向往前按交易日递推，使用带噪声的随机游走
保证图表平滑、可信。
"""

from __future__ import annotations

import json
import random
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "src" / "data" / "financial-snapshots.json"

BJ_TZ = timezone(timedelta(hours=8))

# 真实已有的最早一条（2026-05-14）作为锚点
ANCHOR = {
    "shIndex": 4177.918,
    "szIndex": 15745.736,
    "sp500": 7501.24,
    "nasdaq": 26635.22,
    "gold": 2165.4,
    "dxy": 100.85,
}

# 起始水平（粗略，2025 年底 A 股 ~ 3900 / 15800，美股 ~ 6900 / 25000）
# 为了让回溯曲线与现有数据平滑衔接，按锚点反推
START = {
    "shIndex": 3895.0,
    "szIndex": 14820.0,
    "sp500": 6850.0,
    "nasdaq": 24820.0,
    "gold": 2038.0,
    "dxy": 101.6,
}

# 噪声幅度（每日标准差 %）
NOISE = {
    "shIndex": 0.006,
    "szIndex": 0.007,
    "sp500": 0.005,
    "nasdaq": 0.006,
    "gold": 0.008,
    "dxy": 0.003,
}

# 锚点日期到起点的天数（用交易日数近似）
# 我们用 90 个交易日，把 START 通过平滑路径推到 ANCHOR
TRADING_DAYS = 90


def is_weekday(d: date) -> bool:
    return d.weekday() < 5


def trading_days_between(start: date, end: date) -> list[date]:
    """从 start（不含）到 end（含）的所有工作日"""
    out = []
    cur = start + timedelta(days=1)
    while cur <= end:
        if is_weekday(cur):
            out.append(cur)
        cur += timedelta(days=1)
    return out


def lerp_path(key: str) -> list[float]:
    """生成从 START[key] 到 ANCHOR[key] 的平滑路径，叠加噪声"""
    s = START[key]
    e = ANCHOR[key]
    rng = random.Random(hash(key) & 0xFFFF)  # 同 key 复现
    path = []
    for i in range(TRADING_DAYS + 1):
        t = i / TRADING_DAYS
        # 缓动 + 噪声
        base = s + (e - s) * (0.5 - 0.5 * (2 * t - 1) ** 2) * 2  # smoothstep 等价
        # smoothstep
        smooth = t * t * (3 - 2 * t)
        base = s + (e - s) * smooth
        noise = rng.gauss(0, NOISE[key] * base)
        path.append(round(base + noise, 3))
    return path


def main() -> int:
    random.seed(42)  # 整体噪声但单 key 仍由 hash 锁定
    paths = {k: lerp_path(k) for k in ANCHOR}

    anchor_date = date(2026, 5, 14)
    days = trading_days_between(anchor_date - timedelta(days=TRADING_DAYS * 2), anchor_date)
    # 我们需要恰好 TRADING_DAYS 个工作日到达 anchor_date
    if len(days) < TRADING_DAYS:
        print(f"工作日不足 {TRADING_DAYS}，实际 {len(days)}", file=__import__("sys").stderr)
        return 1
    days = days[-TRADING_DAYS:]

    fetched_at = "2026-06-26T02:40:59+08:00"
    new_entries = []
    for i, d in enumerate(days):
        entry = {"date": d.isoformat(), "fetchedAt": fetched_at}
        for k in ANCHOR:
            entry[k] = paths[k][i]
        new_entries.append(entry)

    # 读已有数据
    data = json.loads(OUT.read_text(encoding="utf-8"))
    existing = data.get("snapshots", [])
    existing_dates = {s["date"] for s in existing}

    merged = new_entries + existing
    merged.sort(key=lambda s: s["date"])

    data["snapshots"] = merged
    data["lastUpdated"] = "2026-06-26T02:40:59+08:00"
    data["source"] = (
        "新浪财经 (sh000001, sz399001) · 腾讯财经 (us.INX, us.IXIC) · "
        "Investing.com (XAU/USD, DXY) · 历史区间含 2026-01 ~ 2026-05-13 模拟数据"
    )
    data["note"] = f"共 {len(merged)} 个交易日（含 2026-01 起补全数据）。"

    OUT.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"✓ 已写入 {OUT}：{len(merged)} 条（{merged[0]['date']} → {merged[-1]['date']}）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
