# 数据库实验课 · DB Lab

面向学生的实验教程与资料站点，采用纯静态 HTML/CSS，可直接部署至 GitHub Pages。无需 Node.js、数据库或构建服务。

## Project 1

- Microsoft Access 入门：建库、建表、Tab 文本导入、SQL 插入、随机数据生成与验证。
- University 数据集：7 张表、371 条原始记录，提供 ZIP 与单文件下载。
- 原始 PPTX、PDF 与两份实验报告模板。
- 提交自查与常见问题。

教程来源为提供的 `Project_0_1.pptx`（第 34–46 页）和数据文件。主键按第 44 页红色标记整理，字段类型为教程建议。网页中的 Microsoft 官方文档链接用于补充操作说明。旧课件的邮箱、日期、评分规则不作为本学期有效通知。

## 本地预览

```sh
python3 -m http.server 8765 --directory docs
```

然后在浏览器打开 `http://localhost:8765`。

## GitHub Pages 发布

在仓库 Settings → Pages 中设置：

- Source：Deploy from a branch
- Branch：main
- Folder：/docs

保存后等待 GitHub Pages 部署成功。以 GitHub Pages 设置页面显示的网站地址为准。

[GitHub 官方配置说明](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)

## 维护

- `docs/index.html`：课程页面、教程、本学期通知和所有下载链接。
- `docs/assets/style.css`：响应式样式。
- `docs/projects/project1/data/`：原始 TXT 数据及 `manifest.json`（记录数、字段、大小、SHA-256）。
- `docs/projects/project1/materials/`：原始课件、数据包与报告模板。
- `scripts/check_site.py`：本地链接、数据行数、主键唯一性、ZIP 与原始文件一致性验证。

更新本学期邮箱和截止日期时，同时更新顶部通知与提交要求。后续项目将资料存入 `docs/projects/projectN/`，添加项目教程页面并更新导航；没有资料的项目保持“待发布”，不要放置无效链接。

## 原始资料

课件与模板保留原始文件内容及其署名。报告中的示例姓名、学号与旧软件环境需由学生替换为自己的信息。未对原始资料额外授予开源许可。
