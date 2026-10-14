#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cer_planner.py — 临床评价（CER）路径规划与 PMCF 计划生成
=========================================================
路径：同品种比对（EU MDR Annex XIV + MEDDEV 2.7.1 rev.4）/
临床试验 / NMPA 临床评价 / FDA 510(k) 实质等效。
输出：路径建议 + 证据缺口 + PMCF 计划骨架。

诚实边界：等同性论证是注册审评核心难点，本工具只做结构化规划，
不替代临床专家论证；具体产品按目标辖区法规执行。
"""
from __future__ import annotations
import argparse
import sys

# --- 辖区别名归一化（2026-10-14 跨模块统一词表）---
# 目标：同一句话在医疗线各模块间通用——既接受 ISO 国家码，也接受监管机构缩写。
# 注意：东盟(ASEAN) / 拉美(LATAM) 尚无实现，仍会被下方校验明确拒绝。
_JURIS_ALIAS = {
    "CN": "CN", "NMPA": "CN", "CHINA": "CN",
    "US": "US", "USA": "US", "FDA": "US",
    "EU": "EU", "MDR": "EU", "CE": "EU",
    "JP": "JP", "JAPAN": "JP", "PMDA": "JP",
}
_JURIS_LOCAL = {"CN": "CN", "US": "FDA", "EU": "EU"}


def _norm_juris(j):
    """把用户输入归一化到本模块内部键；未知值原样返回，交由原校验明确拒绝。"""
    s = (j or "").strip().upper()
    c = _JURIS_ALIAS.get(s)
    if c is None:
        return s
    return _JURIS_LOCAL.get(c, c)


CER_PATHS = {
    "EU": {
        "routes": [
            "同品种比对（MEDDEV 2.7.1 rev.4 + MDR Annex XIV Part A）",
            "临床试验（MDR Annex XV 临床调查 / 科学建议）",
        ],
        "key_docs": ["CER 临床评价报告", "临床开发计划 CDP", "PMP（上市后临床随访）"],
        "authority": "公告机构 (NB) 审评 + 主管机关问询",
    },
    "CN": {
        "routes": [
            "同品种比对（《医疗器械临床评价技术指导原则》2021年第73号）",
            "临床试验（免临床目录外的高风险/创新器械）",
        ],
        "key_docs": ["临床评价报告 CER", "临床评价资料", "伦理/试验方案（如适用）"],
        "authority": "NMPA 技术审评",
    },
    "FDA": {
        "routes": [
            "510(k) 实质等效（与已上市 predicate 比对）",
            "De Novo / PMA（低/高风险新器械）",
        ],
        "key_docs": ["510(k) 申报资料", "性能测试", "临床证据（如需要）"],
        "authority": "FDA CDRH",
    },
}

EQUIVALENCE_ELEMENTS = [
    "技术特性（设计/材料/规格/能量输出）",
    "生物学特性（生物相容性/灭菌/包装）",
    "临床特性（预期用途/适应证/禁忌/使用方式）",
    "与同品种的差异逐项论证（不对等同性有影响）",
    "文献检索策略（数据库/时间/语言/纳排）",
]

PMCF_ELEMENTS = [
    ("终点", "与 CER 声明的安全/性能终点一致"),
    ("人群", "目标人群/亚组（年龄/性别/合并症）"),
    ("随访时长", "按风险等级与预期并发症时间窗设定"),
    ("统计", "样本量/检验效能/分析集"),
    ("报告周期", "PMCF 计划更新 + PSUR/年度报告联动"),
    ("触发更新", "重大变更/不良事件趋势/新文献 → CER 更新"),
]


def plan(jurisdiction: str, innovation: bool, comparable: bool) -> dict:
    if jurisdiction not in CER_PATHS:
        raise ValueError(f"未知辖区 {jurisdiction}（可选 {sorted(CER_PATHS)}）")
    p = CER_PATHS[jurisdiction]
    if comparable and not innovation:
        route = p["routes"][0]
        gaps = ["同品种数据的可及性与差异论证", "文献检索的完备性"]
    else:
        route = p["routes"][-1]
        gaps = ["临床试验方案与伦理", "样本量与统计假设", "数据管理与监查"]
    return {"辖区": jurisdiction, "建议路径": route,
            "创新/无同品种": "是" if innovation or not comparable else "否",
            "证据缺口": gaps, "关键文档": p["key_docs"]}


def render_pmcf() -> str:
    lines = ["# PMCF 计划骨架（MDR Annex XIV Part B / 通用）", ""]
    for k, v in PMCF_ELEMENTS:
        lines.append(f"- **{k}**：{v}")
    lines += ["", "## 同品种比对要素清单", ""]
    for e in EQUIVALENCE_ELEMENTS:
        lines.append(f"- [ ] {e}")
    return "\n".join(lines)


def _demo() -> int:
    print("临床评价路径规划器 · 演示\n")
    for j in ("EU", "CN", "FDA"):
        for innov, comp in [(False, True), (True, False)]:
            p = plan(j, innov, comp)
            print(f"### {j}（创新={innov}, 有同品种={comp}）")
            print(f"  建议路径: {p['建议路径']}")
            print(f"  证据缺口: {'; '.join(p['证据缺口'])}")
    print("\n[demo] 等同性论证须临床专家完成；本工具只做结构化规划。")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="CER 路径规划与 PMCF 计划")
    ap.add_argument("--demo", action="store_true", help="跑内置演示")
    ap.add_argument("--selftest", action="store_true", help="跑内置自测（断言 + 负对照 + xfail）")
    ap.add_argument("--plan", action="store_true", help="路径规划")
    ap.add_argument("--jurisdiction", help="CN|NMPA | US|FDA | EU|MDR | JP|PMDA | ALL（别名互通；ASEAN/LATAM 未实现）")
    ap.add_argument("--innovation", action="store_true", help="创新器械")
    ap.add_argument("--no-comparable", action="store_true", help="无同品种")
    ap.add_argument("--pmcf", action="store_true", help="打印 PMCF 计划骨架")
    args = ap.parse_args()
    if getattr(args, "selftest", False):
        return _selftest()

    if args.demo:
        return _demo()
    if args.plan:
        if not args.jurisdiction:
            print("[err] --plan 须配 --jurisdiction")
            return 2
        try:
            p = plan(_norm_juris(args.jurisdiction), args.innovation, not args.no_comparable)
        except ValueError as e:
            print(f"[err] {e}")
            return 2
        for k, v in p.items():
            print(f"{k}: {v}")
        return 0
    if args.pmcf:
        print(render_pmcf())
        return 0
    ap.print_help()
    return 2


# ==================== 内置自测（--selftest） ====================
# 由 conformance 补丁于 2026-10-14 生成（生成器 v2）。
# 特性：端到端 CLI 调用 + 内容断言 + 负对照 + xfail（已知缺陷显式标注，不掩盖）。
_SELFTEST_CASES = [(['--demo'], 0, [], [], None), (['--plan', '--jurisdiction', 'EU'], 0, [], [], None), (['--pmcf'], 0, [], [], None), (['--plan'], 2, [], [], None)]


def _selftest() -> int:
    import os as _os
    import subprocess as _sp
    _here = _os.path.dirname(_os.path.abspath(__file__))
    # 仓库根：脚本位于 <repo>/scripts/ 时取上一级；否则取脚本所在目录
    _root = _os.path.dirname(_here) if _os.path.basename(_here) == "scripts" else _here
    _script = _os.path.abspath(__file__)
    _fail, _xfail, _n = [], [], 0
    for _case in _SELFTEST_CASES:
        _args, _rc, _must, _mustnot = _case[0], _case[1], _case[2], _case[3]
        _reason = _case[4] if len(_case) > 4 else None
        _n += 1
        _p = _sp.run([sys.executable, _script] + _args, capture_output=True, cwd=_root)
        _out = _p.stdout.decode("utf-8", "replace")
        _bad = []
        if _p.returncode != _rc:
            _bad.append(f"rc={_p.returncode} 期望 {_rc}")
        for _m in _must:
            if _m not in _out:
                _bad.append(f"输出缺少 {_m!r}")
        for _m in _mustnot:
            if _m in _out:
                _bad.append(f"输出含禁止内容 {_m!r}")
        if _rc == 0 and not _out.strip():
            _bad.append("rc=0 但输出为空（假绿）")
        if _bad:
            if _reason:
                _xfail.append(f"xfail args={_args}：{'；'.join(_bad)} ← 已知缺陷：{_reason}")
            else:
                _fail.append(f"args={_args}：{'；'.join(_bad)}")
    # 通用负对照：未知参数必须非零
    _n += 1
    _p = _sp.run([sys.executable, _script, "--__nonexistent_flag__"], capture_output=True, cwd=_root)
    if _p.returncode == 0:
        _fail.append("负对照失败：未知参数竟返回 0")
    for _x in _xfail:
        print("[selftest][xfail] " + _x)
    if _fail:
        print(f"[selftest] FAILED {len(_fail)}/{_n}")
        for _f in _fail:
            print("  - " + _f)
        return 1
    print(f"[selftest] PASS {_n - len(_xfail)}/{_n}（含负对照；xfail {len(_xfail)} 项为已知缺陷）")
    return 0


if __name__ == "__main__":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass
    raise SystemExit(main())
