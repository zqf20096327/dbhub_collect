# -*- coding: utf-8 -*-
"""一次性把 interp_cache 拆成分片（方案 A：sha256(key) 前 2 位 → 256 桶）。

用法（在仓库根目录）：
  python tools/split_interp_cache.py             # merge：并集落分片，保留旧单文件（安全，可反复跑）
  python tools/split_interp_cache.py --cutover   # 收口：落分片后删旧单文件及其 .1-.4 轮转副本

切换时序：先 merge（老代码/新代码并存无碍，读取端是并集），
等 CI 空闲 + 本地无旧代码进程在跑时再 --cutover，随代码切换同一个提交推上去。
自带校验：拆完重新 load_cache() 与拆分前 dict 逐键比对，不等即报错退出码 1。
"""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "lib"))
import interp_store as st  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description="interp_cache 单文件 → 256 分片")
    ap.add_argument("--cutover", action="store_true",
                    help="落分片后删除旧单文件及轮转副本（正式切换时用）")
    args = ap.parse_args()

    before = st.load_cache()
    bad_keys = [k for k in before if len(k) < 2]
    if bad_keys:
        print(f"异常：{len(bad_keys)} 个 key 长度 <2 无法分桶，样例 {bad_keys[:3]}")
        return 1

    n_buckets = st.save_cache_all(before)
    after = st.load_cache()
    if after != before:
        only_before = {k for k in before if k not in after}
        only_after = {k for k in after if k not in before}
        diff_val = sum(1 for k in before if k in after and before[k] != after[k])
        print(f"校验失败：丢 {len(only_before)} 增 {len(only_after)} 值异 {diff_val}"
              f"（样例丢 {list(only_before)[:3]}）")
        return 1

    total_mb = sum(p.stat().st_size for p in st.SHARD_DIR.glob("*.json")) / 1e6
    print(f"分片 OK：{len(before)} 条 → {n_buckets} 桶，共 {total_mb:.1f} MB，"
          f"逐键校验一致，旧单文件保留")

    # 倾斜报警（10-06 加）：桶字节 max/中位 > 5 判异常退出——防未来 key 格式
    # 漂移（如新前缀类 key）静默挤爆个别桶，重演 desc:: 案（299 条挤 de 桶）。
    sizes = sorted(p.stat().st_size for p in st.SHARD_DIR.glob("*.json"))
    if sizes:
        med = sizes[len(sizes) // 2]
        if med > 0 and sizes[-1] / med > 5:
            print(f"倾斜报警：最大桶 {sizes[-1] / 1e3:.0f}KB 是中位 {med / 1e3:.0f}KB 的 "
                  f"{sizes[-1] / med:.1f} 倍（阈值 5）——检查是否有带前缀的 key 形态",
                  file=sys.stderr)
            return 1
        print(f"桶分布：中位 {med / 1e3:.0f}KB，最大 {sizes[-1] / 1e3:.0f}KB"
              f"（{sizes[-1] / med:.1f}×中位）")

    if args.cutover:
        for p in [st.LEGACY] + [st.LEGACY.with_suffix(f".json.{i}") for i in (1, 2, 3, 4)] \
                 + [st.LEGACY.with_suffix(".json.tmp")]:
            if p.is_file():
                p.unlink()
                print(f"cutover：删除 {p.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
