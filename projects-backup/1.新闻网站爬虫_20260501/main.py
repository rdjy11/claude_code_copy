"""国际新闻爬虫 - 从央视网、人民网、环球网、新华网抓取当天国际新闻，输出 HTML 页面"""
import sys
import io
import os
import webbrowser
import requests
from bs4 import BeautifulSoup
import re
import json
from datetime import datetime

# Windows 控制台 UTF-8 支持
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# ========== 抓取函数 ==========

def fetch_cctv():
    articles = []
    for page in range(1, 4):
        url = f"https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/world_{page}.jsonp"
        try:
            resp = requests.get(url, headers=HEADERS, timeout=10)
            resp.encoding = "utf-8"
            match = re.search(r"world\((.+)\)", resp.text, re.DOTALL)
            if not match:
                continue
            data = json.loads(match.group(1))
            for item in data["data"]["list"]:
                img = item.get("image", "")
                articles.append({
                    "title": item["title"],
                    "url": item["url"],
                    "summary": item.get("brief", ""),
                    "time": item.get("focus_date", ""),
                    "source": "央视网",
                    "image": img if img and img.startswith("http") else ""
                })
        except Exception as e:
            print(f"  [央视网] 第{page}页抓取失败: {e}")
    return articles


def fetch_people():
    articles = []
    try:
        resp = requests.get("http://world.people.com.cn/", headers=HEADERS, timeout=10)
        resp.encoding = "utf-8"
        soup = BeautifulSoup(resp.text, "html.parser")

        for item in soup.select(".hdNews.clearfix"):
            strong = item.select_one("strong a")
            em = item.select_one("em.gray2 a")
            if strong:
                title = strong.get_text(strip=True)
                href = strong.get("href", "")
                url = "http://world.people.com.cn" + href if href.startswith("/") else href
                summary = em.get_text(strip=True) if em else ""
                articles.append({
                    "title": title, "url": url, "summary": summary,
                    "time": "", "source": "人民网", "image": ""
                })

        for a_tag in soup.select(".list_14 a, .list_14b a"):
            title = a_tag.get_text(strip=True)
            href = a_tag.get("href", "")
            if title and "http" in href:
                articles.append({
                    "title": title, "url": href, "summary": "",
                    "time": "", "source": "人民网", "image": ""
                })
    except Exception as e:
        print(f"  [人民网] 抓取失败: {e}")
    return articles


def fetch_huanqiu():
    articles = []
    seen = set()
    try:
        resp = requests.get("https://world.huanqiu.com/", headers=HEADERS, timeout=10)
        resp.encoding = "utf-8"
        soup = BeautifulSoup(resp.text, "html.parser")
        data_container = soup.select_one(".data-container")
        if not data_container:
            print("  [环球网] 未找到数据容器")
            return articles

        for item in data_container.select(".item"):
            aid_el = item.select_one(".item-aid")
            title_el = item.select_one(".item-title")
            time_el = item.select_one(".item-time")
            addltype_el = item.select_one(".item-addltype")
            cover_el = item.select_one(".item-cover")

            if not aid_el or not title_el:
                continue

            aid = aid_el.get_text(strip=True)
            title = title_el.get_text(strip=True)
            if not title or aid in seen:
                continue
            seen.add(aid)

            ts = time_el.get_text(strip=True) if time_el else ""
            if ts and ts.isdigit():
                ts = datetime.fromtimestamp(int(ts) / 1000).strftime("%Y-%m-%d %H:%M:%S")

            addltype = addltype_el.get_text(strip=True) if addltype_el else "article"
            url = f"https://world.huanqiu.com/{addltype}/{aid}"

            img = cover_el.get_text(strip=True) if cover_el else ""
            if img and not img.startswith("http"):
                img = "https:" + img

            articles.append({
                "title": title, "url": url, "summary": "",
                "time": ts, "source": "环球网", "image": img
            })
    except Exception as e:
        print(f"  [环球网] 抓取失败: {e}")
    return articles


def fetch_xinhua():
    articles = []
    seen = set()
    try:
        resp = requests.get("https://www.news.cn/world/", headers=HEADERS, timeout=10)
        resp.encoding = "utf-8"
        soup = BeautifulSoup(resp.text, "html.parser")

        for item in soup.select(".column-center-item"):
            for a_tag in item.select(".tit a"):
                title = a_tag.get_text(strip=True)
                href = a_tag.get("href", "")
                if not title or not href or title in seen:
                    continue
                seen.add(title)
                if any(kw in title for kw in ["专题", "|", "更多"]):
                    continue
                articles.append({
                    "title": title, "url": href, "summary": "",
                    "time": "", "source": "新华网", "image": ""
                })
    except Exception as e:
        print(f"  [新华网] 抓取失败: {e}")
    return articles


# ========== HTML 生成 ==========

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>国际新闻汇总 - {date}</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif; background: #f5f6fa; color: #222; }}
a {{ text-decoration: none; color: inherit; }}

/* 顶栏 */
.header {{ background: linear-gradient(135deg, #1a1d23 0%, #2c3038 100%); padding: 16px 0; position: sticky; top: 0; z-index: 100; }}
.header-inner {{ max-width: 1000px; margin: 0 auto; padding: 0 24px; display: flex; align-items: center; gap: 24px; }}
.header .logo {{ font-size: 22px; font-weight: 700; color: #fff; }}
.header .logo span {{ color: #ff6b3d; }}
.header .date {{ color: #999; font-size: 13px; margin-left: auto; }}

/* 导航标签 */
.tabs {{ max-width: 1000px; margin: 24px auto 0; padding: 0 24px; display: flex; gap: 4px; }}
.tab {{ padding: 9px 22px; border-radius: 6px 6px 0 0; font-size: 14px; cursor: pointer; color: #888; background: #e8e9ee; transition: all .2s; border: none; }}
.tab:hover {{ color: #555; background: #ddd; }}
.tab.active {{ color: #fff; background: #ff6b3d; font-weight: 600; }}

/* 主容器 */
.container {{ max-width: 1000px; margin: 0 auto; padding: 0 24px 40px; }}

/* 双栏 */
.main-content {{ display: flex; gap: 24px; }}

/* 左栏 */
.news-list {{ flex: 1; min-width: 0; }}
.source-header {{ padding: 20px 0 12px; font-size: 18px; font-weight: 700; color: #333; border-bottom: 2px solid #ff6b3d; margin-bottom: 16px; }}
.source-header em {{ font-style: normal; color: #ff6b3d; }}
.source-header .count {{ font-size: 13px; color: #999; font-weight: 400; margin-left: 8px; }}

/* 新闻卡片 */
.news-card {{ display: flex; gap: 16px; padding: 16px; margin-bottom: 1px; background: #fff; transition: background .15s; }}
.news-card:hover {{ background: #fafbfc; }}
.news-card:first-of-type {{ border-radius: 8px 8px 0 0; }}
.news-card:last-of-type {{ border-radius: 0 0 8px 8px; margin-bottom: 0; }}
.news-card:only-of-type {{ border-radius: 8px; }}
.news-card .thumb {{ width: 180px; height: 110px; border-radius: 4px; object-fit: cover; flex-shrink: 0; background: #eee; }}
.news-card .no-thumb {{ width: 180px; height: 110px; border-radius: 4px; flex-shrink: 0; background: #f0f1f4; display: flex; align-items: center; justify-content: center; color: #ccc; font-size: 36px; }}
.news-card .body {{ flex: 1; min-width: 0; display: flex; flex-direction: column; }}
.news-card .body .title {{ font-size: 16px; font-weight: 600; line-height: 1.5; color: #222; margin-bottom: 8px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }}
.news-card .body .title:hover {{ color: #ff6b3d; }}
.news-card .body .summary {{ font-size: 13px; line-height: 1.7; color: #777; flex: 1; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }}
.news-card .body .meta {{ font-size: 12px; color: #bbb; margin-top: 8px; display: flex; align-items: center; gap: 12px; }}
.news-card .body .meta .source-tag {{ display: inline-block; padding: 2px 8px; border-radius: 3px; font-size: 11px; color: #ff6b3d; background: #fff3ef; }}

/* 右栏 */
.sidebar {{ width: 260px; flex-shrink: 0; }}
.sidebar-card {{ background: #fff; border-radius: 8px; padding: 16px; margin-bottom: 16px; }}
.sidebar-card h3 {{ font-size: 15px; font-weight: 700; color: #333; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 2px solid #ff6b3d; }}
.sidebar-card .stat-item {{ display: flex; justify-content: space-between; padding: 6px 0; font-size: 13px; color: #666; }}
.sidebar-card .stat-item .num {{ font-weight: 700; color: #ff6b3d; }}
.sidebar-card .hot-item {{ display: block; padding: 7px 0; font-size: 13px; color: #555; line-height: 1.4; border-bottom: 1px solid #f5f5f5; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
.sidebar-card .hot-item:hover {{ color: #ff6b3d; }}
.sidebar-card .hot-item:last-child {{ border-bottom: none; }}
.sidebar-card .hot-item .idx {{ display: inline-block; width: 18px; height: 18px; line-height: 18px; text-align: center; border-radius: 3px; font-size: 11px; color: #fff; background: #ccc; margin-right: 6px; }}
.sidebar-card .hot-item:nth-child(1) .idx,
.sidebar-card .hot-item:nth-child(2) .idx,
.sidebar-card .hot-item:nth-child(3) .idx {{ background: #ff6b3d; }}

/* 页脚 */
.footer {{ text-align: center; padding: 24px; color: #bbb; font-size: 12px; }}

/* 响应式 */
@media (max-width: 768px) {{
  .main-content {{ flex-direction: column; }}
  .sidebar {{ width: 100%; }}
  .news-card .thumb, .news-card .no-thumb {{ width: 120px; height: 76px; }}
}}
</style>
</head>
<body>

<div class="header">
  <div class="header-inner">
    <div class="logo">国际<span>新闻</span>速览</div>
    <div class="date">{date}</div>
  </div>
</div>

<div class="tabs">
  {tabs}
</div>

<div class="container">
  <div class="main-content">
    <div class="news-list">
      {news_items}
    </div>
    <div class="sidebar">
      {sidebar}
    </div>
  </div>
</div>

<div class="footer">
  数据来源：央视网 · 人民网 · 环球网 · 新华网 ｜ 自动抓取于 {date}
</div>

<script>
(function() {{
  var tabs = document.querySelectorAll('.tab');
  var panels = document.querySelectorAll('.source-panel');
  var sidebarPanels = document.querySelectorAll('.sidebar-panel');
  tabs.forEach(function(tab) {{
    tab.addEventListener('click', function() {{
      var src = this.dataset.source;
      tabs.forEach(function(t) {{ t.classList.remove('active'); }});
      this.classList.add('active');
      panels.forEach(function(p) {{ p.style.display = 'none'; }});
      (document.getElementById('panel-' + src) || panels[0]).style.display = '';
      sidebarPanels.forEach(function(p) {{ p.style.display = 'none'; }});
      (document.getElementById('sidebar-' + src) || sidebarPanels[0]).style.display = '';
    }});
  }});
}})();
</script>

</body>
</html>"""


def generate_html(all_articles):
    today = datetime.now().strftime("%Y-%m-%d")
    by_source = {}
    for a in all_articles:
        by_source.setdefault(a["source"], []).append(a)

    sources = ["央视网", "人民网", "环球网", "新华网"]
    source_labels = {"央视网": "cctv", "人民网": "people", "环球网": "huanqiu", "新华网": "xinhua"}

    # 标签栏
    tabs = []
    for i, src in enumerate(sources):
        active = 'active' if i == 0 else ''
        tabs.append(f'<button class="tab {active}" data-source="{source_labels[src]}">{src}</button>')
    tabs_html = "\n  ".join(tabs)

    # 新闻列表
    news_html = ""
    for si, src in enumerate(sources):
        items = by_source.get(src, [])
        display = '' if si == 0 else 'style="display:none"'
        news_html += f'<div class="source-panel" id="panel-{source_labels[src]}" {display}>\n'
        news_html += f'<div class="source-header"><em>{src}</em><span class="count">共 {len(items)} 条</span></div>\n'
        for a in items:
            img_html = ""
            if a.get("image"):
                img_html = f'<img class="thumb" src="{a["image"]}" referrerpolicy="no-referrer" loading="lazy" onerror="this.style.display=\'none\'">'
            else:
                img_html = '<div class="no-thumb">&#x1F4F0;</div>'

            time_html = f'<span>{a["time"]}</span>' if a["time"] else ""
            summary = a["summary"].replace("<", "&lt;").replace(">", "&gt;") if a["summary"] else ""

            news_html += f"""<a class="news-card" href="{a["url"]}" target="_blank">
  {img_html}
  <div class="body">
    <div class="title">{a["title"]}</div>
    {f'<div class="summary">{summary}</div>' if summary else ''}
    <div class="meta"><span class="source-tag">{a["source"]}</span>{time_html}</div>
  </div>
</a>
"""
        news_html += "</div>\n"

    # 侧栏
    sidebar = ""
    for si, src in enumerate(sources):
        items = by_source.get(src, [])
        display = '' if si == 0 else 'style="display:none"'
        item_count = len(items)

        # Top 8 hot items
        hot = ""
        for j, a in enumerate(items[:8]):
            hot += f'<a class="hot-item" href="{a["url"]}" target="_blank"><span class="idx">{j+1}</span>{a["title"]}</a>\n'

        sidebar += f"""<div class="sidebar-panel" id="sidebar-{source_labels[src]}" {display}>
<div class="sidebar-card">
  <h3>📊 来源统计</h3>
  <div class="stat-item"><span>新闻总数</span><span class="num">{item_count}</span></div>
  <div class="stat-item"><span>有摘要</span><span class="num">{sum(1 for a in items if a["summary"])}</span></div>
  <div class="stat-item"><span>有配图</span><span class="num">{sum(1 for a in items if a.get("image"))}</span></div>
</div>
<div class="sidebar-card">
  <h3>🔥 本来源热榜</h3>
  {hot}
</div>
</div>
"""

    # 总统计侧栏
    total = len(all_articles)
    with_img = sum(1 for a in all_articles if a.get("image"))
    with_summary = sum(1 for a in all_articles if a["summary"])

    sidebar += f"""<div class="sidebar-card">
  <h3>📈 全局统计</h3>
  <div class="stat-item"><span>新闻总数</span><span class="num">{total}</span></div>
  <div class="stat-item"><span>覆盖来源</span><span class="num">{len(sources)}</span></div>
  <div class="stat-item"><span>有摘要</span><span class="num">{with_summary}</span></div>
  <div class="stat-item"><span>有配图</span><span class="num">{with_img}</span></div>
</div>"""

    html = HTML_TEMPLATE.format(
        date=today,
        tabs=tabs_html,
        news_items=news_html,
        sidebar=sidebar
    )
    return html


def main():
    print("正在抓取国际新闻...")

    all_articles = []

    print("\n[1/4] 央视网...")
    all_articles.extend(fetch_cctv())

    print("[2/4] 人民网...")
    all_articles.extend(fetch_people())

    print("[3/4] 环球网...")
    all_articles.extend(fetch_huanqiu())

    print("[4/4] 新华网...")
    all_articles.extend(fetch_xinhua())

    # 去重（按URL）
    seen_urls = set()
    deduped = []
    for a in all_articles:
        if a["url"] not in seen_urls:
            seen_urls.add(a["url"])
            deduped.append(a)

    by_source = {}
    for a in deduped:
        by_source.setdefault(a["source"], []).append(a)

    print(f"\n抓取完成：央视网 {len(by_source.get('央视网',[]))} | "
          f"人民网 {len(by_source.get('人民网',[]))} | "
          f"环球网 {len(by_source.get('环球网',[]))} | "
          f"新华网 {len(by_source.get('新华网',[]))} | "
          f"共 {len(deduped)} 条")

    # 生成 HTML
    print("\n生成 HTML...")
    html = generate_html(deduped)

    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               f"news_{datetime.now().strftime('%Y%m%d')}.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"已保存: {output_path}")

    # 打开浏览器
    webbrowser.open("file:///" + output_path.replace("\\", "/"))
    print("已在浏览器中打开。")


if __name__ == "__main__":
    main()
