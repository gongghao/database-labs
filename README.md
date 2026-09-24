# 数据库实验课

学生入口：https://gongghao.github.io/database-labs/

## 课程安排

所有时间均为北京时间（Asia/Shanghai）。

| 内容 | 发布 | 提交截止 |
| --- | --- | --- |
| 实验准备 | 现在开放 | 无 |
| Project 1 | 2026-10-05 00:00 | 2026-10-19 00:00，即 10 月 18 日结束前 |
| Project 2–6 | 待通知 | 待通知 |

提交邮箱 / 平台以本学期通知为准；原始课件中的旧日期与邮箱不适用。

## 发布方式与公开范围

仓库保持公开。GitHub Actions 按服务器时间生成 `_site/`，未开放项目只生成状态页，不向网站部署题目或下载文件。学生修改设备时间无法提前打开网页内容。Project 1 的材料此前已经公开，仍可从本仓库及历史记录取得，因此网页锁定不构成对这些旧材料的保密措施。

Project 2–6 的完整教程与附件暂时保留在助教本地，未上传此公开仓库。确定发布日期后，再上传相应内容并修改 `config/course.json`。`.gitignore` 防止默认添加本地未发布资料；发布时需明确选择文件。

`docs/` 保留原已公开的 Project 1 材料，仅作为构建输入。网站必须选择 **Settings → Pages → Source → GitHub Actions**，不得继续从 `docs/` 直接发布。

## 维护

- `config/course.json`：发布日期与截止日期；`null` 表示待通知，一直锁定。
- `content/preparation.html`：实验准备；`content/project1.html`：Project 1 教程。
- `public/assets/style.css`：网站样式。
- `scripts/build_site.py`：生成发布目录。
- `tests/test_release.py`：开放边界、链接与文件完整性检查。
- `.github/workflows/pages.yml`：测试、构建与部署。

```sh
python3 -m unittest discover -s tests -v
python3 scripts/build_site.py
python3 -m http.server 8765 --bind 127.0.0.1 --directory _site
```

仅预览与发布 `_site/`，不要公开整个本地工作目录，也不要发布未来时间的测试产物。

工作流在推送、手动触发及每日北京时间 00:00 执行，在已确定的开放与截止边界另有重试。GitHub 的定时任务可能延迟，不能保证零点即时上线，但构建不会提前放出网页内容。截止后保留资料供复习；本站展示提交时间，不接收作业。

Project 3 使用官方 JDK / Maven 下载链接，原始大型安装程序留在本地。Project 4、6 需自行设计业务测试数据。
