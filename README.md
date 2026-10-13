# clinical-evaluation

> **Contributed by [@stevenzhao07](https://github.com/stevenzhao07) · Affiliation: MedXpert (medical-device RA & regulatory consultancy) · Pure technical input, no commercial promotion.**

临床评价（CER）路径规划与 PMCF 计划生成：同品种比对（EU MDR Annex XIV + MEDDEV 2.7.1 rev.4）、临床试验路径、NMPA 临床评价指导原则路径、FDA 510(k) 实质等效；PMCF 计划模板（终点/人群/随访/统计）与 PSUR/CER 更新触发条件。

这是 MedXpert 把"医疗 AI 信任"方法论工程化落地的可插拔模块之一——把抽象的合规要求变成一条可重复运行的命令或参考实现。方法论四要素（白话版）：**治理守护者 XCGS** ＝ 为 AI 留下可核验的治理证据；**立法者 A³ Laws** ＝ 给自主系统划权限 / 监督 / 追责三条硬边界；**护照官 AI 护照** ＝ 为模型签发可追溯的身份凭证；**人机共存** ＝ 明确人类与 AI 的分工与兜底。

---

## 可插拔模块契约（lgd-skeleton/1.0）

本仓库是一个 **`lgd-skeleton/1.0` 可插拔模块**：

- **一切即插件**：仅依赖声明式 `module.json`，零配置；
- **按需装（lazy）**：仅 triggers 命中时加载；
- **可嵌套（nested）**：可被 `medical-ai-toolkit` 总入口路由发现；
- **扩展点**：`plugins/`(新增辖区路径：在 CER_PATHS 加一项。)。

机器可发现入口：`AGENTS.md` · `CLAUDE.md` · `llms.txt`。

## 特性

- 路径判定器：按器械类别/创新性/同品种可得性给出路径建议与证据缺口
- 同品种比对要素清单（特性/差异/等同性论证/文献检索策略）
- PMCF 计划模板：终点、人群、随访时长、统计方法、报告周期
- 更新触发：变更/不良事件趋势/新文献 → CER 更新评估

**上游投稿目标**：OpenRegulatory/templates

## 内容说明

同品种路径的等同性论证是注册审评核心难点，本工具只做结构化规划，不替代临床专家论证。

## 免责声明

本工具仅提供结构化模板与计算能力，**不构成法规建议、临床建议或产品合规结论**。具体产品的注册、临床评价、灭菌验证、风险分析、软件分级等决策，须由合资格人员依据目标辖区（NMPA / FDA / EU MDR / PMDA）最新法规文本作出；条款与限值以官方发布文本为准。使用本工具产生的一切后果由使用者自行承担。

## 使用

```bash
python scripts/cer_planner.py --demo
python scripts/cer_planner.py --pmcf
```

## 快速开始（30 秒）

```bash
git clone https://github.com/stevenzhao07/clinical-evaluation.git && cd clinical-evaluation
python scripts/cer_planner.py --demo
```

> 想参与或遇到问题？[提 Issue](https://github.com/stevenzhao07/clinical-evaluation/issues) · 完整《AI 参与指南》见 [medical-ai-toolkit](https://github.com/stevenzhao07/medical-ai-toolkit)。

## 路由（总入口）

本模块由 **[medical-ai-toolkit](https://github.com/stevenzhao07/medical-ai-toolkit)** 作为 `lgd-skeleton/1.0` 总入口自动路由发现。

## 关联模块

- [device-regulatory-map](https://github.com/stevenzhao07/device-regulatory-map)
- [pms-vigilance](https://github.com/stevenzhao07/pms-vigilance)
- [ml-validation-toolkit](https://github.com/stevenzhao07/ml-validation-toolkit)

## 许可

CC-BY-4.0 — 见 [LICENSE](./LICENSE)。

## 关联（方法论来源）

- 理念溯源：个人专家关于医疗 AI 信任与治理的公开方法论（个人观点，不构成标准）
- 同账号系列：见 `medical-ai-toolkit` 导航
