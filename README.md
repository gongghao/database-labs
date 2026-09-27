# 数据库实验课 · 2026 秋季

学生入口：https://gongghao.github.io/database-labs/

课程信息：https://gongghao.github.io/database-labs/course.html

作业提交与答疑邮箱：**seudatabaseqa@gmail.com**。

## 课程信息

B09D0013 · Databases，授课教师 Prof. Shuai Wang，助教 Hao Gong。
上课时间为周一 09:50–12:15，第 1–14 周，教室 J3-502。

依据 `Databases_2026_Fall_syllabusV3.0.doc`：考试占 70%，平时测验与项目占 30%；迟交 1 天计 90%，2 天计 80%，3 天及以上计 50%。Grace Days 通过课堂活动获取，具体使用方法以课堂说明为准。

## 项目日程

所有时间均为北京时间（Asia/Shanghai）00:00；请在截止日前一天结束前提交。

| 内容 | 发布 | 提交截止 |
| --- | --- | --- |
| 实验准备 | 现在开放 | 无 |
| Project 1 | 2026-10-05 | 2026-10-19 |
| Project 2 | 2026-10-19 | 2026-11-02 |
| Project 3 | 2026-11-02 | 2026-11-16 |
| Project 4 | 2026-11-16 | 2026-11-30 |
| Project 5 | 2026-11-30 | 2026-12-14 |
| Project 6 | 2026-12-14 | 待通知，与期末考试安排一并确定 |

第 11 次课在原大纲中误写为 12/30，已由助教确认更正为 **11/30**。网站采用更正日期，供下载的原文件保留原文。

## 发布方式与公开范围

仓库保持公开，仓库中的文件和历史可被直接访问。GitHub Actions 按服务器时间生成 `_site/`，未开放项目只生成状态页，不向网站部署题目和附件。网页按日期开放不构成对公开仓库源文件的访问限制。

`docs/` 保留原已公开的 Project 1 材料，仅作为构建输入。网站选择 **Settings → Pages → Source → GitHub Actions**，不从 `docs/` 直接发布。

## 维护

- `config/course.json`：发布日期与截止日期；`null` 表示待通知。
- `content/preparation.html`：独立实验准备页。
- `content/course.html`：邮箱、考核、教材、上课信息与教学计划。
- `content/projectN.html`：各项目教程；`content/projects/projectN/`：资料。
- `config/assets.json`：已纳入仓库的原始附件校验清单。
- `public/assets/style.css`：网站样式。
- `scripts/build_site.py`：生成发布目录。
- `tests/test_release.py`：开放边界、链接与文件完整性检查。
- `.github/workflows/pages.yml`：测试、构建与部署。

```sh
python3 -m unittest discover -s tests -v
python3 scripts/build_site.py
python3 -m http.server 8765 --bind 127.0.0.1 --directory _site
```

仅发布 `_site/`，不要发布未来时间的测试产物。

工作流在推送、手动触发及每日北京时间 00:00 执行，在 00:17、00:37 重试。GitHub 的定时任务可能延迟，不能保证零点即时上线，但构建不会提前放出网页内容。截止后保留资料供复习；本站展示提交时间，作业通过邮箱提交。

成功部署后，工作流仅在项目开放或截止状态变化时更新 `config/release-state.json`；这既记录课程状态，也保持学期内仓库活动，避免公开仓库连续 60 天无活动导致 GitHub 停用定时工作流。此文件不参与开放判定，实际判定始终依据课程配置和服务器时间。

Project 3 使用官方 JDK / Maven 下载链接，原始大型安装程序留在本地。Project 4、6 需自行设计业务测试数据。
