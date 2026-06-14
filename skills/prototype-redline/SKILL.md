---
name: prototype-redline
description: 为 HTML 原型嵌入可视化标注系统——支持新生成时自动嵌入，也支持为已有 HTML 文件注入和移除。用户在浏览器框选区域、添加备注、导出 JSON 反馈给 Claude 迭代。触发词：加标注、帮我标注、annotate、给这个 HTML 加标注、我要标注这个原型、去掉标注、移除标注、remove annotator。
---

# HTML 标注系统 Skill

## 三大工作场景（速查）

| 触发信号 | 场景 | 执行路径 |
|---------|------|---------|
| 用户说"加标注"/"帮我标注"/"annotate"，并提供文件路径 | **A：注入已有文件** | 见下方场景A步骤 |
| 用户要求生成供审阅/评审的 HTML 原型 | **B：新生成时嵌入** | 见下方场景B步骤 |
| 用户消息中含有 `"annotations":[` 的 JSON 内容 | **C：解析标注迭代** | 见"收到 JSON 后处理" |
| 用户说"去掉标注"/"移除标注"/"remove annotator" | **D：移除标注系统** | 见下方场景D步骤 |

**不嵌入**的情况：纯图表/数据可视化、生产代码 HTML 模板（除非用户明确要求）。

---

### 场景A：注入已有 HTML 文件

1. **Read** 读取文件完整内容（失败 → 告知用户"文件路径不对或无法访问"，结束）
2. **查重**：文件中已含 `_ann_btn` → 告知用户无需重复注入，结束
3. **Edit** 在 `</body>` 前插入下方代码块（无 `</body>` 则追加末尾）
4. **告知**：文件已更新，在浏览器刷新即可使用

### 场景B：生成新 HTML 原型时

1. 生成 HTML 内容
2. 在 `</body>` 前插入下方代码块
3. 回复末尾附上「使用说明」（让用户知道如何操作标注系统）

### 场景D：移除标注系统

**触发词**："去掉标注"、"移除标注"、"remove annotator"、"把标注系统删掉"

1. **Read** 读取文件完整内容（失败 → 告知文件路径不对，结束）
2. **查重**：文件中不含 `_ann_btn` → 告知用户"文件中未找到标注系统"，结束
3. **Edit** 删除从 `<!-- HTML Annotator` 到其后对应 `</script>` 的完整代码块（含前后空行）
4. **告知**：标注系统已移除，在浏览器刷新即可

## 嵌入方式

在 HTML 文件 `</body>` 标签前插入以下完整代码块：

```html
<!-- HTML Annotator — 框选区域后输入备注，点"复制 JSON"把反馈发给 Claude -->
<script>
(function () {
  var anns = [], idCtr = 1, active = false, dragging = false;
  var sx, sy, drawEl, pendingRect, uiDrag = null;

  /* ── 样式 ── */
  var s = document.createElement('style');
  s.textContent = [
    '@keyframes _ann_pulse{0%,100%{box-shadow:-3px 2px 18px rgba(102,126,234,.5)}50%{box-shadow:-4px 2px 32px rgba(102,126,234,.9),0 0 0 5px rgba(102,126,234,.12)}}',
    '#_ann_tb{position:fixed;right:0;top:45%;z-index:2147483647;user-select:none}',
    '#_ann_btn{display:flex;flex-direction:column;align-items:center;gap:3px;background:linear-gradient(160deg,#667eea,#764ba2);color:#fff;border:none;padding:14px 8px 14px 14px;border-radius:16px 0 0 16px;cursor:pointer;font-size:22px;line-height:1;font-family:-apple-system,sans-serif;transform:translateX(55%);transition:transform .25s cubic-bezier(.34,1.56,.64,1);animation:_ann_pulse 2.5s ease-in-out infinite}',
    '#_ann_btn span{font-size:9px;letter-spacing:1px;opacity:.9;white-space:nowrap}',
    '#_ann_tb:hover #_ann_btn,#_ann_btn.on{transform:translateX(0);animation:none}',
    '#_ann_btn.on{background:linear-gradient(160deg,#c53030,#e53e3e)}',
    '#_ann_ov{position:fixed;inset:0;z-index:2147483640;cursor:crosshair;pointer-events:none}',
    '#_ann_ov.on{pointer-events:all}',
    '._ann_r{position:fixed;border:2px solid #e53e3e;background:rgba(229,62,62,.07);z-index:2147483641;pointer-events:none}',
    '._ann_b{position:absolute;top:-10px;left:-10px;background:#e53e3e;color:#fff;width:20px;height:20px;border-radius:50%;display:flex;align-items:center;justify-content:center;font:bold 11px sans-serif}',
    '#_ann_panel{position:fixed;bottom:14px;right:14px;width:290px;background:#fff;border-radius:10px;box-shadow:0 4px 20px rgba(0,0,0,.18);z-index:2147483647;display:none;font:13px/1.4 -apple-system,sans-serif;overflow:hidden}',
    '#_ann_panel.on{display:block}',
    '#_ann_ph{padding:11px 14px;background:#1a1a2e;color:#fff;font-weight:600;display:flex;justify-content:space-between;cursor:move}',
    '#_ann_pb{max-height:220px;overflow-y:auto}',
    '._ann_item{padding:8px 14px;border-bottom:1px solid #f0f0f0;font-size:12px;color:#333}',
    '._ann_n{display:inline-flex;align-items:center;justify-content:center;background:#e53e3e;color:#fff;width:18px;height:18px;border-radius:50%;font-size:10px;font-weight:bold;margin-right:6px;flex-shrink:0}',
    '#_ann_pf{padding:9px 14px;display:flex;gap:7px;border-top:1px solid #eee}',
    '._ann_fbtn{flex:1;padding:6px;border:none;border-radius:5px;cursor:pointer;font-size:12px;font-weight:500}',
    '#_ann_copy{background:#1a1a2e;color:#fff}',
    '#_ann_clr{background:#fff5f5;color:#c53030;border:1px solid #fed7d7}',
    '#_ann_tip{padding:7px 14px 8px;font-size:11px;color:#999;border-top:1px solid #f0f0f0;line-height:1.6}',
    '#_ann_bbl{position:fixed;z-index:2147483647;background:#fff;border-radius:8px;box-shadow:0 4px 16px rgba(0,0,0,.18);padding:11px;width:230px;display:none;font:13px -apple-system,sans-serif}',
    '#_ann_bbl_hdr{cursor:move;text-align:center;color:#bbb;font-size:11px;margin-bottom:7px;user-select:none;letter-spacing:2px}',
    '#_ann_ta{width:100%;border:1px solid #e2e8f0;border-radius:5px;padding:6px 8px;font-size:12px;resize:none;outline:none;box-sizing:border-box;font-family:inherit}',
    '#_ann_bbl_btns{display:flex;gap:10px;margin-top:9px}',
    '#_ann_bbl_btns button{flex:1;padding:7px 5px;border:none;border-radius:4px;cursor:pointer;font-size:12px}',
    '#_ann_ok{background:#1a1a2e;color:#fff}',
    '#_ann_no{background:#f7fafc;color:#555}'
  ].join('');
  document.head.appendChild(s);

  /* ── DOM ── */
  function el(tag, id, html) {
    var e = document.createElement(tag);
    if (id) e.id = id;
    if (html) e.innerHTML = html;
    document.body.appendChild(e);
    return e;
  }

  var ov     = el('div', '_ann_ov');
  var tb     = el('div', '_ann_tb', '<button id="_ann_btn">📌<span>标注</span></button>');
  var panel  = el('div', '_ann_panel',
    '<div id="_ann_ph"><span>标注列表</span><span id="_ann_cnt">0 条</span></div>' +
    '<div id="_ann_pb"></div>' +
    '<div id="_ann_tip">📋 完成后点「复制 JSON」，粘贴到 Claude 对话框，他会按标注修改原型</div>' +
    '<div id="_ann_pf">' +
    '<button class="_ann_fbtn" id="_ann_copy">复制 JSON</button>' +
    '<button class="_ann_fbtn" id="_ann_clr">清空</button></div>');
  var bbl    = el('div', '_ann_bbl',
    '<div id="_ann_bbl_hdr">⠿ ⠿ ⠿</div>' +
    '<textarea id="_ann_ta" rows="3" placeholder="描述偏差（Shift+Enter 换行，Enter 确认）"></textarea>' +
    '<div id="_ann_bbl_btns"><button id="_ann_ok">确认</button><button id="_ann_no">取消</button></div>');

  /* ── 拖移 ── */
  function makeDraggable(elem, handle, vOnly) {
    handle.addEventListener('mousedown', function (e) {
      if (e.button !== 0 || e.target.tagName === 'TEXTAREA') return;
      var isBtn = e.target.tagName === 'BUTTON';
      var r = elem.getBoundingClientRect();
      var ox = e.clientX - r.left, oy = e.clientY - r.top;
      var sx = e.clientX, sy = e.clientY;
      function mm(ev) {
        if (!uiDrag && (Math.abs(ev.clientX - sx) + Math.abs(ev.clientY - sy) > 5)) {
          uiDrag = { el: elem, ox: ox, oy: oy, vOnly: !!vOnly };
          if (isBtn) {
            e.target.addEventListener('click', function stop(ce) {
              ce.stopImmediatePropagation();
              e.target.removeEventListener('click', stop, true);
            }, true);
          }
        }
      }
      function mu() {
        document.removeEventListener('mousemove', mm);
        document.removeEventListener('mouseup', mu);
      }
      document.addEventListener('mousemove', mm);
      document.addEventListener('mouseup', mu);
      if (!isBtn) e.preventDefault();
    });
  }
  makeDraggable(tb, tb, true);
  makeDraggable(panel, document.getElementById('_ann_ph'));
  makeDraggable(bbl, document.getElementById('_ann_bbl_hdr'));

  /* ── 切换标注模式 ── */
  document.getElementById('_ann_btn').onclick = function () {
    active = !active;
    this.classList.toggle('on', active);
    this.innerHTML = active ? '✕' : '📌<span>标注</span>';
    ov.classList.toggle('on', active);
  };

  /* ── 画框 ── */
  ov.addEventListener('mousedown', function (e) {
    if (!active) return;
    dragging = true; sx = e.clientX; sy = e.clientY;
    drawEl = document.createElement('div');
    drawEl.className = '_ann_r';
    drawEl.style.cssText = 'left:' + sx + 'px;top:' + sy + 'px;width:0;height:0';
    document.body.appendChild(drawEl);
  });

  document.addEventListener('mousemove', function (e) {
    if (uiDrag) {
      var ny = Math.max(0, Math.min(e.clientY - uiDrag.oy, window.innerHeight - uiDrag.el.offsetHeight));
      uiDrag.el.style.top = ny + 'px';
      if (!uiDrag.vOnly) {
        var nx = Math.max(0, Math.min(e.clientX - uiDrag.ox, window.innerWidth - uiDrag.el.offsetWidth));
        uiDrag.el.style.left = nx + 'px';
        uiDrag.el.style.right = 'auto'; uiDrag.el.style.bottom = 'auto';
      }
      return;
    }
    if (!dragging || !drawEl) return;
    var x = Math.min(e.clientX, sx), y = Math.min(e.clientY, sy);
    var w = Math.abs(e.clientX - sx), h = Math.abs(e.clientY - sy);
    drawEl.style.cssText = 'left:' + x + 'px;top:' + y + 'px;width:' + w + 'px;height:' + h + 'px';
  });

  document.addEventListener('mouseup', function (e) {
    if (uiDrag) { uiDrag = null; return; }
    if (!dragging) return;
    dragging = false;
    var x = Math.min(e.clientX, sx), y = Math.min(e.clientY, sy);
    var w = Math.abs(e.clientX - sx), h = Math.abs(e.clientY - sy);
    if (w < 8 || h < 8) { if (drawEl) { drawEl.remove(); drawEl = null; } return; }
    pendingRect = { x: x, y: y, w: w, h: h, el: drawEl };
    drawEl = null;
    /* 显示输入气泡 */
    var bx = Math.min(x + w + 8, window.innerWidth - 248);
    var by = Math.max(8, Math.min(y, window.innerHeight - 170));
    bbl.style.cssText = 'display:block;left:' + bx + 'px;top:' + by + 'px';
    var ta = document.getElementById('_ann_ta');
    ta.value = ''; ta.focus();
  });

  /* ── 确认备注 ── */
  function save() {
    var text = document.getElementById('_ann_ta').value.trim();
    if (!text || !pendingRect) {
      if (pendingRect) { pendingRect.el.remove(); pendingRect = null; }
      bbl.style.display = 'none'; return;
    }
    var id = idCtr++;
    var vw = window.innerWidth, vh = window.innerHeight;
    /* 捕获页面和元素上下文 */
    var cx = Math.round(pendingRect.x + pendingRect.w / 2);
    var cy = Math.round(pendingRect.y + pendingRect.h / 2);
    ov.style.pointerEvents = 'none';
    var tel = document.elementFromPoint(cx, cy);
    ov.style.pointerEvents = '';
    var telStr = '';
    if (tel) {
      telStr = tel.tagName.toLowerCase();
      if (tel.id) { telStr += '#' + tel.id; }
      else if (tel.className && typeof tel.className === 'string') {
        var cls = tel.className.trim().split(/\s+/).slice(0, 2).join('.');
        if (cls) telStr += '.' + cls;
      }
    }
    /* 向上查找最近的有 id 的祖先，用于定位 JS render 函数 */
    var nearestId = '';
    var cur = tel;
    while (cur && cur !== document.body) {
      if (cur.id && !cur.id.startsWith('_ann_')) { nearestId = cur.id; break; }
      cur = cur.parentElement;
    }
    var ap = document.querySelector('.page.active');
    anns.push({
      id: id,
      x: Math.round(pendingRect.x),
      y: Math.round(pendingRect.y),
      width: Math.round(pendingRect.w),
      height: Math.round(pendingRect.h),
      x_pct: +(pendingRect.x / vw * 100).toFixed(1),
      y_pct: +(pendingRect.y / vh * 100).toFixed(1),
      w_pct: +(pendingRect.w / vw * 100).toFixed(1),
      h_pct: +(pendingRect.h / vh * 100).toFixed(1),
      page_id: ap ? ap.id : '',
      nearest_id: nearestId,
      target_el: telStr,
      comment: text
    });
    /* 贴编号 */
    var badge = document.createElement('div');
    badge.className = '_ann_b'; badge.textContent = id;
    pendingRect.el.appendChild(badge);
    bbl.style.display = 'none'; pendingRect = null;
    refresh();
  }

  document.getElementById('_ann_ok').onclick = save;
  document.getElementById('_ann_ta').addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); save(); }
  });
  document.getElementById('_ann_no').onclick = function () {
    if (pendingRect) { pendingRect.el.remove(); pendingRect = null; }
    bbl.style.display = 'none';
  };

  /* ── 面板刷新 ── */
  function refresh() {
    document.getElementById('_ann_cnt').textContent = anns.length + ' 条';
    document.getElementById('_ann_pb').innerHTML = anns.map(function (a) {
      return '<div class="_ann_item"><span class="_ann_n">' + a.id + '</span>' + a.comment + '</div>';
    }).join('');
    panel.classList.toggle('on', anns.length > 0);
  }

  /* ── 复制 JSON（兼容 file:// 协议） ── */
  function fallbackCopy(text, btn) {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.style.cssText = 'position:fixed;top:-9999px;left:-9999px';
    document.body.appendChild(ta);
    ta.select();
    try {
      document.execCommand('copy');
      btn.textContent = '已复制 ✓';
    } catch (e) {
      btn.textContent = '复制失败';
    }
    document.body.removeChild(ta);
    setTimeout(function () { btn.textContent = '复制 JSON'; }, 2000);
  }
  document.getElementById('_ann_copy').onclick = function () {
    var btn = this;
    var json = JSON.stringify({
      timestamp: new Date().toISOString(),
      viewport: { width: window.innerWidth, height: window.innerHeight },
      annotations: anns
    }, null, 2);
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(json).then(function () {
        btn.textContent = '已复制 ✓';
        setTimeout(function () { btn.textContent = '复制 JSON'; }, 2000);
      }).catch(function () { fallbackCopy(json, btn); });
    } else {
      fallbackCopy(json, btn);
    }
  };

  /* ── 清空 ── */
  document.getElementById('_ann_clr').onclick = function () {
    anns = []; idCtr = 1;
    document.querySelectorAll('._ann_r').forEach(function (el) { el.remove(); });
    refresh();
  };
})();
</script>
```

---

## 场景C：收到用户标注 JSON 后如何处理

**触发条件**：用户消息中含有 `"annotations":[` 字段的 JSON 内容（无论是否有其他文字）。

字段速查：
```
nearest_id — 标注元素向上最近的有 id 的祖先（首选定位锚点）
page_id    — 激活的 .page.active 的 id（次选）
target_el  — 标注中心点的 DOM 元素描述（如 "button.btn.bt"）
comment    — 用户描述
```

**定位规则（按优先级）：**
1. `nearest_id` 非空 → Grep 该 id 在源码中的写入位置（innerHTML 赋值、render 函数体）
2. `nearest_id` 为空且 `target_el` 含 `#id` → Grep 该 id
3. 均无 id → Grep `target_el` 类名在 JS 模板字符串中的位置
4. 以上均失败 → 根据 `x_pct/y_pct` 估算所在区域，告知用户："定位不精确，估算是 [区域描述]，请确认是否是这里？"，等用户确认后再修改

**异常与边界：**

| 情况 | 处理 |
|---|---|
| JSON 格式损坏（无法解析）| 回复"JSON 看起来不完整，请重新点原型里的'复制 JSON'按钮后再粘贴" |
| `annotations` 数组为空 | 回复"标注列表是空的，请先在浏览器框选区域添加标注，再点'复制 JSON'" |
| 某条标注缺 `comment` 字段 | 跳过该条，汇报末尾注明"标注 #N 无描述已跳过" |
| 定位规则4触发（所有 id 为空）| 先告知估算区域和候选元素，明确等用户回复"对"/"不是"后再动代码 |

**修改后务必保留标注系统代码**：若迭代时重写了整个 HTML，检查输出是否仍包含 `_ann_btn`；若遗漏，在写回前补入代码块。

修改完成后告知每条改动（一行一条，无需解释过程）：
```
已根据你的 3 条标注完成修改：
① 右上角导航区：将背景色从 #f5f5f5 改为 #1a1a2e
② 中部卡片区：标题字号从 14px 调整为 18px
③ 底部按钮：改为主色填充，去掉描边样式
```

---

## 使用说明（给用户看）

将以下文字在首次使用时告知用户：

> **使用标注系统：**
> 1. 在浏览器打开 HTML 文件
> 2. 点页面右侧边缘的 **📌 标注** 悬浮按钮（鼠标移过去会滑出）进入标注模式
> 3. 在页面上拖拽框选有问题的区域
> 4. 松开鼠标后输入备注，按 Enter 确认
> 5. 重复标注其他区域
> 6. 点右下角面板的 **复制 JSON**
> 7. 把复制的内容粘回对话，我来修改

---

## 资源文件

| 路径 | 用途 |
|---|---|
| `test-prompts.json` | 3 个典型测试用例（注入/接收JSON/生成原型） |
| `annotator-test.html` | 可直接在浏览器打开的功能验证页面（含完整标注系统） |
