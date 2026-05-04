---
name: 国际新闻爬虫
description: Python 爬虫，从央视网/人民网/环球网/新华网抓取国际新闻，输出腾讯新闻风格 HTML 页面
type: project
originSessionId: f5033295-7782-4ca1-b595-5af96ecc871c
---
项目位于 `E:\.Claude Code Project\1.新闻网站爬虫_20260501\`。

## 功能

从 4 个来源抓取当天国际新闻，输出 HTML 页面并自动在浏览器中打开：
- **央视网** — JSONP API (`news.cctv.com`)，分 3 页抓取，有摘要和配图
- **人民网** — HTML 解析 (`world.people.com.cn`)
- **环球网** — HTML 解析 (`world.huanqiu.com`)，时间戳转换
- **新华网** — HTML 解析 (`www.news.cn/world`)

## 架构

单文件脚本 `main.py`，约 430 行，包含：
- 4 个抓取函数（独立异常处理，互不阻塞）
- URL 去重（跨源去重）
- HTML 模板引擎（腾讯新闻风格：橙红配色、卡片布局、来源标签切换、侧栏统计）
- 自动生成 `news_YYYYMMDD.html` 并在浏览器中打开

## 运行

```bash
cd "E:\.Claude Code Project\1.新闻网站爬虫_20260501"
pip install requests beautifulsoup4   # 首次
python main.py
```

## 输出

- `news_YYYYMMDD.html` — 新闻页面（主输出）
- `news_output_YYYY-MM-DD.txt` — 控制台输出日志
- `debug_*.html` — 各源原始 HTML 调试快照

## 已知问题

- **人民网乱码**：输出为锟斤拷乱码，虽然已设置 `resp.encoding = "utf-8"`，但该页面实际编码可能仍是 GB2312/GBK，尚未彻底解决
- **环球网仅 19 条**：静态 HTML 中只嵌入了部分数据，完整数据需 JS 渲染或 API
- **新华网无时间/摘要**：仅抓取了标题和链接
- **不建议集成飞书推送**（用户已确认暂不需要）

## 唤醒词

「新闻爬虫」「抓新闻」「国际新闻」「跑爬虫」「新闻网站爬虫」
