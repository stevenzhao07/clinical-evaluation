# AGENTS.md · clinical-evaluation

> 机器可发现入口（AI 编码代理 / Codex / Claude / Cursor）。单一事实源：本文件。

## 这是什么
临床评价（CER）路径规划与 PMCF 计划生成：同品种比对（EU MDR Annex XIV + MEDDEV 2.7.1 rev.4）、临床试验路径、NMPA 临床评价指导原则路径、FDA 510(k) 实质等效；PMCF 计划模板（终点/人群/随访/统计）与 PSUR/CER 更新触发条件。

## 运行
```bash
python scripts/cer_planner.py --demo
python scripts/cer_planner.py --help
```

## 扩展契约（lgd-skeleton/1.0）
- **一切即插件**：仅依赖声明式 `module.json`，零配置。
- **按需装（lazy）**：仅 triggers 命中时加载。
- **可嵌套（nested）**：可被 `medical-ai-toolkit` 总入口路由。
- **扩展点**：`plugins/`(新增辖区路径：在 CER_PATHS 加一项。)

## 红线
纯技术贡献，不含商业营销；MedXpert 仅作为贡献者署名（@stevenzhao07）。
