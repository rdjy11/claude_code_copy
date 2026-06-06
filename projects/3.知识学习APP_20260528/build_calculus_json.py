#!/usr/bin/env python3
"""构建微积分完整课程 JSON（机械工业出版社教材体系）
第1-3章: 函数与极限、导数与微分、中值定理与导数应用
"""
import json, os

# Python raw strings 或普通字符串中 \x 不会被视为 hex escape
# 因为 Python 只识别 \xhh（两个 hex digits）格式

content = {
  "course_id": "calculus",
  "course_name": "微积分",
  "subject_id": "math",
  "structure_type": "hierarchical",
  "chapters": [
    # ===== 第1章: 函数与极限 (4节, 7知识点, 15题) =====
    {
      "id": "calc_ch01",
      "title": "第一章 函数与极限",
      "sections": [
        {
          "id": "calc_sec01",
          "title": "1.1 函数的概念与性质",
          "knowledge_points": [
            {
              "id": "calc_kp001",
              "title": "函数的定义与表示",
              "content_type": "markdown",
              "content": "## 函数的定义\n\n设 $X$ 和 $Y$ 是两个非空集合。若存在对应法则 $f$，使对于 $X$ 中每个 $x$，$Y$ 中有**唯一**确定的 $y$ 与之对应，则称 $f$ 是从 $X$ 到 $Y$ 的**函数**：\n\n$$y = f(x), \\quad x \\in X$$\n\n**定义域**：$x$ 的取值范围。**值域**：全体 $f(x)$ 的取值。\n\n### 三种表示方法\n- 解析法（公式法）：$y = x^2 + 1$\n- 列表法：用表格列出对应值\n- 图像法：在坐标平面上画出曲线",
              "key_concepts": ["定义域","值域","对应法则","解析法","列表法","图像法"],
              "quizzes": [
                {"id":"calc_q001","type":"single_choice","question":"若 $f(x)=x^2+1$，则 $f(-2)$ 的值为？","options":[{"key":"A","text":"3"},{"key":"B","text":"5"},{"key":"C","text":"-3"},{"key":"D","text":"4"}],"answer":"B","explanation":"代入 $x=-2$：$f(-2)=(-2)^2+1=4+1=5$。"},
                {"id":"calc_q002","type":"single_choice","question":"函数 $f(x)=\\frac{1}{x-1}$ 的定义域是？","options":[{"key":"A","text":"$(-\\infty,+\\infty)$"},{"key":"B","text":"$(-\\infty,1)\\cup(1,+\\infty)$"},{"key":"C","text":"$[1,+\\infty)$"},{"key":"D","text":"$(0,+\\infty)$"}],"answer":"B","explanation":"分母不能为零，所以 $x-1\\neq 0$，即 $x\\neq 1$。"},
                {"id":"calc_q003","type":"single_choice","question":"函数 $y=\\sqrt{x-2}$ 的定义域是？","options":[{"key":"A","text":"$x\\geq 0$"},{"key":"B","text":"$x\\geq 2$"},{"key":"C","text":"$x>2$"},{"key":"D","text":"$x\\leq 2$"}],"answer":"B","explanation":"根号下表达式必须非负：$x-2\\geq 0$，解得 $x\\geq 2$。"}
              ]
            },
            {
              "id": "calc_kp002",
              "title": "函数的奇偶性与周期性",
              "content_type": "markdown",
              "content": "## 函数的奇偶性\n\n### 偶函数\n若 $f(-x)=f(x)$，则 $f(x)$ 是**偶函数**，图像关于 $y$ 轴对称。常见：$y=x^2$，$y=\\cos x$，$y=|x|$。\n\n### 奇函数\n若 $f(-x)=-f(x)$，则 $f(x)$ 是**奇函数**，图像关于原点对称。若 $f(0)$ 有定义，必有 $f(0)=0$。常见：$y=x^3$，$y=\\sin x$。\n\n### 周期性\n若存在 $T>0$ 使 $f(x+T)=f(x)$ 对所有 $x$ 成立，则 $f(x)$ 为**周期函数**，$T$ 为**周期**。",
              "key_concepts": ["偶函数","奇函数","原点对称","周期函数","最小正周期"],
              "quizzes": [
                {"id":"calc_q004","type":"single_choice","question":"函数 $f(x)=x^2\\cos x$ 的奇偶性是？","options":[{"key":"A","text":"奇函数"},{"key":"B","text":"偶函数"},{"key":"C","text":"非奇非偶"},{"key":"D","text":"既是奇函数也是偶函数"}],"answer":"B","explanation":"$x^2$ 和 $\\cos x$ 都是偶函数，偶函数 $\\times$ 偶函数 = 偶函数。"},
                {"id":"calc_q005","type":"single_choice","question":"若 $f(x)$ 是奇函数且 $f(2)=3$，则 $f(-2)$ 等于？","options":[{"key":"A","text":"3"},{"key":"B","text":"-3"},{"key":"C","text":"0"},{"key":"D","text":"无法确定"}],"answer":"B","explanation":"奇函数定义 $f(-x)=-f(x)$，所以 $f(-2)=-f(2)=-3$。"}
              ]
            },
            {
              "id": "calc_kp003",
              "title": "基本初等函数与复合函数",
              "content_type": "markdown",
              "content": "## 基本初等函数\n\n1. **幂函数**：$y=x^\\alpha$（$\\alpha$ 为常数）\n2. **指数函数**：$y=a^x$（$a>0,a\\neq 1$），定义域 $(-\\infty,+\\infty)$，值域 $(0,+\\infty)$\n3. **对数函数**：$y=\\log_a x$（$a>0,a\\neq 1$），定义域 $(0,+\\infty)$\n4. **三角函数**：$\\sin x$，$\\cos x$，$\\tan x$ 等\n5. **反三角函数**：$\\arcsin x$，$\\arccos x$，$\\arctan x$ 等\n\n## 复合函数\n\n设 $y=f(u), u=g(x)$。若 $g(x)$ 的值域与 $f(u)$ 的定义域交集非空，则 $y=f[g(x)]$ 称为**复合函数**，$u$ 为中间变量。\n\n## 初等函数\n\n由基本初等函数经过有限次四则运算和复合运算得到的能用一个解析式表示的函数。",
              "key_concepts": ["幂函数","指数函数","对数函数","反三角函数","复合函数","初等函数"],
              "quizzes": [
                {"id":"calc_q006","type":"single_choice","question":"函数 $y=\\ln(x-1)$ 的定义域是？","options":[{"key":"A","text":"$(0,+\\infty)$"},{"key":"B","text":"$[1,+\\infty)$"},{"key":"C","text":"$(1,+\\infty)$"},{"key":"D","text":"$(-\\infty,1)$"}],"answer":"C","explanation":"对数函数要求真数 $>0$，即 $x-1>0$，解得 $x>1$。"},
                {"id":"calc_q007","type":"single_choice","question":"$y=\\sin(x^2)$ 是由哪些函数复合而成？","options":[{"key":"A","text":"$y=\\sin u, u=x^2$"},{"key":"B","text":"$y=\\sin x, u=x^2$"},{"key":"C","text":"$y=u, u=\\sin(x^2)$"},{"key":"D","text":"无法复合"}],"answer":"A","explanation":"外层函数 $y=\\sin u$，内层函数 $u=x^2$，复合得 $y=\\sin(x^2)$。"}
              ]
            }
          ]
        },
        {
          "id": "calc_sec02",
          "title": "1.2 数列的极限",
          "knowledge_points": [
            {
              "id": "calc_kp004",
              "title": "数列极限的定义与性质",
              "content_type": "markdown",
              "content": "## 数列极限的 $\\varepsilon$-$N$ 定义\n\n设 $\\{x_n\\}$ 为数列，$a$ 为常数。若对任意 $\\varepsilon>0$，总存在正整数 $N$，使当 $n>N$ 时恒有：\n\n$$|x_n-a|<\\varepsilon$$\n\n则称 $a$ 是数列 $\\{x_n\\}$ 的**极限**，记作 $\\lim_{n\\to\\infty}x_n=a$。\n\n## 收敛数列的性质\n\n1. **唯一性**：收敛数列的极限唯一\n2. **有界性**：收敛数列必有界\n3. **保号性**：若 $\\lim x_n=a>0$，则 $n$ 充分大时 $x_n>0$\n4. **四则运算**：若 $\\lim x_n=a,\\lim y_n=b$，则 $\\lim(x_n\\pm y_n)=a\\pm b$，$\\lim x_ny_n=ab$，当 $b\\neq 0$ 时 $\\lim\\frac{x_n}{y_n}=\\frac{a}{b}$\n5. **夹逼准则**：若 $y_n\\leq x_n\\leq z_n$ 且 $\\lim y_n=\\lim z_n=a$，则 $\\lim x_n=a$",
              "key_concepts": ["ε-N定义","收敛","发散","有界性","夹逼准则"],
              "quizzes": [
                {"id":"calc_q008","type":"single_choice","question":"$\\lim_{n\\to\\infty}\\frac{1}{n}$ 等于？","options":[{"key":"A","text":"1"},{"key":"B","text":"0"},{"key":"C","text":"不存在"},{"key":"D","text":"$\\infty$"}],"answer":"B","explanation":"这是最基本的收敛数列，$\\lim_{n\\to\\infty}\\frac{1}{n}=0$。"},
                {"id":"calc_q009","type":"single_choice","question":"下列哪个数列发散？","options":[{"key":"A","text":"$x_n=\\frac{1}{n}$"},{"key":"B","text":"$x_n=(-1)^n$"},{"key":"C","text":"$x_n=\\frac{n}{n+1}$"},{"key":"D","text":"$x_n=2^{-n}$"}],"answer":"B","explanation":"$x_n=(-1)^n$ 在 1 和 -1 间震荡，不收敛。其余均收敛。"}
              ]
            }
          ]
        },
        {
          "id": "calc_sec03",
          "title": "1.3 函数的极限",
          "knowledge_points": [
            {
              "id": "calc_kp005",
              "title": "函数极限与左右极限",
              "content_type": "markdown",
              "content": "## 函数极限的 $\\varepsilon$-$\\delta$ 定义\n\n若对任意 $\\varepsilon>0$，存在 $\\delta>0$，使当 $0<|x-x_0|<\\delta$ 时 $|f(x)-A|<\\varepsilon$，则称 $\\lim_{x\\to x_0}f(x)=A$。\n\n## 左极限与右极限\n- **左极限**：$\\lim_{x\\to x_0^{-}}f(x)$，$x$ 从 $x_0$ 左侧趋近\n- **右极限**：$\\lim_{x\\to x_0^{+}}f(x)$，$x$ 从 $x_0$ 右侧趋近\n\n$$\\lim_{x\\to x_0}f(x)=A \\iff \\lim_{x\\to x_0^{-}}f(x)=\\lim_{x\\to x_0^{+}}f(x)=A$$\n\n## 函数极限运算法则\n若 $\\lim f(x)=A$，$\\lim g(x)=B$，则：\n- $\\lim[f(x)\\pm g(x)]=A\\pm B$\n- $\\lim[f(x)\\cdot g(x)]=A\\cdot B$\n- $\\lim\\frac{f(x)}{g(x)}=\\frac{A}{B}$（$B\\neq 0$）\n- $\\lim[cf(x)]=cA$（$c$ 为常数）",
              "key_concepts": ["ε-δ定义","左极限","右极限","极限运算法则"],
              "quizzes": [
                {"id":"calc_q010","type":"single_choice","question":"$\\lim_{x\\to 0^+}\\frac{|x|}{x}$ 等于？","options":[{"key":"A","text":"1"},{"key":"B","text":"-1"},{"key":"C","text":"0"},{"key":"D","text":"不存在"}],"answer":"A","explanation":"当 $x>0$ 时 $|x|=x$，所以右极限为 1。左极限为 -1，双侧极限不存在。"},
                {"id":"calc_q011","type":"single_choice","question":"$\\lim_{x\\to 0}\\frac{\\sin x}{x}$ 等于？（重要极限）","options":[{"key":"A","text":"0"},{"key":"B","text":"1"},{"key":"C","text":"不存在"},{"key":"D","text":"$\\infty$"}],"answer":"B","explanation":"$\\lim_{x\\to 0}\\frac{\\sin x}{x}=1$，是微积分最重要的极限之一，可用夹逼准则证明。"}
              ]
            },
            {
              "id": "calc_kp006",
              "title": "无穷小与无穷大",
              "content_type": "markdown",
              "content": "## 无穷小\n\n若 $\\lim f(x)=0$（在某过程中），则称 $f(x)$ 为该过程中的**无穷小**。\n\n### 无穷小的比较（设 $\\alpha,\\beta$ 为同一过程的无穷小，$\\alpha\\neq 0$）\n- $\\lim\\frac{\\beta}{\\alpha}=0$ → $\\beta$ 是比 $\\alpha$ **高阶的无穷小**，记 $\\beta=o(\\alpha)$\n- $\\lim\\frac{\\beta}{\\alpha}=c\\neq 0$ → $\\beta$ 与 $\\alpha$ **同阶无穷小**\n- $\\lim\\frac{\\beta}{\\alpha}=1$ → $\\beta$ 与 $\\alpha$ **等价无穷小**，记 $\\alpha\\sim\\beta$\n\n### 常见等价无穷小（$x\\to 0$ 时）\n- $\\sin x\\sim x$，$\\tan x\\sim x$\n- $1-\\cos x\\sim\\frac{x^2}{2}$\n- $\\ln(1+x)\\sim x$，$e^x-1\\sim x$\n- $\\arcsin x\\sim x$，$\\arctan x\\sim x$\n\n## 无穷大\n若 $|f(x)|$ 无限增大，称 $f(x)$ 为**无穷大**，记 $\\lim f(x)=\\infty$。无穷大的倒数为无穷小。",
              "key_concepts": ["无穷小","高阶无穷小","等价无穷小","同阶无穷小","无穷大"],
              "quizzes": [
                {"id":"calc_q012","type":"single_choice","question":"当 $x\\to 0$ 时，与 $x$ 等价的是？","options":[{"key":"A","text":"$\\sin x$"},{"key":"B","text":"$1-\\cos x$"},{"key":"C","text":"$x^2$"},{"key":"D","text":"$\\sqrt{x}$"}],"answer":"A","explanation":"$\\sin x\\sim x$。$1-\\cos x\\sim\\frac{x^2}{2}$ 是二阶无穷小，$x^2$ 是二阶，$\\sqrt{x}$ 是 $\\frac{1}{2}$ 阶。"},
                {"id":"calc_q013","type":"single_choice","question":"$\\lim_{x\\to 0}(1+x)^{\\frac{1}{x}}$ 等于？（重要极限）","options":[{"key":"A","text":"0"},{"key":"B","text":"1"},{"key":"C","text":"$e$"},{"key":"D","text":"$\\infty$"}],"answer":"C","explanation":"$\\lim_{x\\to 0}(1+x)^{\\frac{1}{x}}=e$，等价于 $\\lim_{n\\to\\infty}(1+\\frac{1}{n})^n=e$。"}
              ]
            }
          ]
        },
        {
          "id": "calc_sec04",
          "title": "1.4 函数的连续性与间断点",
          "knowledge_points": [
            {
              "id": "calc_kp007",
              "title": "连续与间断",
              "content_type": "markdown",
              "content": "## 连续的定义\n\n若 $\\lim_{x\\to x_0}f(x)=f(x_0)$，则称 $f(x)$ 在 $x_0$ 处**连续**。等价三条件：$f(x_0)$ 有定义；$\\lim_{x\\to x_0}f(x)$ 存在；极限值等于函数值。\n\n## 间断点的分类\n\n**第一类间断点**（左右极限均存在）：\n- 可去间断点：左右极限相等但 $\\neq f(x_0)$\n- 跳跃间断点：左右极限不相等\n\n**第二类间断点**（至少一个单侧极限不存在）：\n- 无穷间断点\n- 振荡间断点\n\n## 闭区间连续函数的性质\n\n1. **有界性与最值定理**：在 $[a,b]$ 上连续的函数必有界且能取到最大值和最小值\n2. **介值定理**：能取到两端点函数值之间的任何值\n3. **零点定理**：若 $f(a)\\cdot f(b)<0$，则存在 $\\xi\\in(a,b)$ 使 $f(\\xi)=0$",
              "key_concepts": ["连续","可去间断","跳跃间断","介值定理","零点定理"],
              "quizzes": [
                {"id":"calc_q014","type":"single_choice","question":"函数 $f(x)=\\begin{cases}\\frac{\\sin x}{x},&x\\neq 0\\\\1,&x=0\\end{cases}$ 在 $x=0$ 处是？","options":[{"key":"A","text":"连续"},{"key":"B","text":"可去间断"},{"key":"C","text":"跳跃间断"},{"key":"D","text":"无穷间断"}],"answer":"A","explanation":"$\\lim_{x\\to 0}\\frac{\\sin x}{x}=1=f(0)$，满足连续定义。"},
                {"id":"calc_q015","type":"single_choice","question":"$f$ 在 $[0,1]$ 连续，$f(0)=-1$，$f(1)=2$，则方程 $f(x)=0$ 在 $(0,1)$ 内？","options":[{"key":"A","text":"可能有根"},{"key":"B","text":"一定有根"},{"key":"C","text":"一定无根"},{"key":"D","text":"无法确定"}],"answer":"B","explanation":"零点定理：$f(0)f(1)=-2<0$ 且 $f$ 连续，故存在 $\\xi\\in(0,1)$ 使 $f(\\xi)=0$。"}
              ]
            }
          ]
        }
      ]
    },
    # ===== 第2章: 导数与微分 (3节, 4知识点, 7题) =====
    {
      "id": "calc_ch02",
      "title": "第二章 导数与微分",
      "sections": [
        {
          "id": "calc_sec05",
          "title": "2.1 导数的概念",
          "knowledge_points": [
            {
              "id": "calc_kp008",
              "title": "导数的定义与几何意义",
              "content_type": "markdown",
              "content": "## 导数的定义\n\n$$f'(x_0)=\\lim_{\\Delta x\\to 0}\\frac{f(x_0+\\Delta x)-f(x_0)}{\\Delta x}=\\lim_{x\\to x_0}\\frac{f(x)-f(x_0)}{x-x_0}$$\n\n若该极限存在，称 $f$ 在 $x_0$ 处**可导**。\n\n### 几何意义\n$f'(x_0)$ = 曲线在 $(x_0,f(x_0))$ 处的**切线斜率**。切线方程：$y-f(x_0)=f'(x_0)(x-x_0)$。\n\n### 可导与连续的关系\n可导 $\\implies$ 连续；连续 $\\not\\implies$ 可导（如 $y=|x|$ 在 $x=0$ 处）。\n\n### 基本求导公式\n| $f(x)$ | $f'(x)$ |\n|--------|--------|\n| $C$ | $0$ |\n| $x^n$ | $nx^{n-1}$ |\n| $e^x$ | $e^x$ |\n| $\\ln x$ | $\\frac{1}{x}$ |\n| $\\sin x$ | $\\cos x$ |\n| $\\cos x$ | $-\\sin x$ |",
              "key_concepts": ["导数定义","差商极限","切线斜率","可导与连续","基本求导公式"],
              "quizzes": [
                {"id":"calc_q016","type":"single_choice","question":"$f(x)=x^2$ 在 $x=1$ 处的导数 $f'(1)$ 等于？","options":[{"key":"A","text":"1"},{"key":"B","text":"2"},{"key":"C","text":"0"},{"key":"D","text":"3"}],"answer":"B","explanation":"$f'(x)=2x$，$f'(1)=2$。或用定义：$\\lim_{h\\to 0}\\frac{(1+h)^2-1}{h}=2$。"},
                {"id":"calc_q017","type":"single_choice","question":"若 $f'(x_0)=0$，曲线在 $x_0$ 处的切线是？","options":[{"key":"A","text":"斜向上"},{"key":"B","text":"斜向下"},{"key":"C","text":"水平直线"},{"key":"D","text":"竖直直线"}],"answer":"C","explanation":"斜率 $k=f'(x_0)=0$，斜率为 0 的直线是水平直线。$x_0$ 可能是驻点。"}
              ]
            }
          ]
        },
        {
          "id": "calc_sec06",
          "title": "2.2 求导法则与高阶导数",
          "knowledge_points": [
            {
              "id": "calc_kp009",
              "title": "四则运算求导与链式法则",
              "content_type": "markdown",
              "content": "## 四则运算法则\n设 $u(x),v(x)$ 可导：\n- $(u\\pm v)'=u'\\pm v'$\n- $(uv)'=u'v+uv'$\n- $(\\frac{u}{v})'=\\frac{u'v-uv'}{v^2}$（$v\\neq 0$）\n\n## 链式法则（复合函数求导）\n若 $y=f(u),u=g(x)$ 均可导，则：\n\n$$\\frac{dy}{dx}=f'[g(x)]\\cdot g'(x)$$\n\n**口诀**：\"由外到内，逐层求导再相乘\"。\n\n## 隐函数求导\n方程 $F(x,y)=0$ 确定 $y=y(x)$，两边对 $x$ 求导，解出 $y'$。\n\n## 参数方程求导\n设 $\\begin{cases}x=\\varphi(t)\\\\y=\\psi(t)\\end{cases}$，则 $\\frac{dy}{dx}=\\frac{\\psi'(t)}{\\varphi'(t)}$。",
              "key_concepts": ["乘法法则","商法则","链式法则","隐函数求导","参数方程求导"],
              "quizzes": [
                {"id":"calc_q018","type":"single_choice","question":"$y=\\ln \\cos x$ 的导数 $y'$ 等于？","options":[{"key":"A","text":"$\\tan x$"},{"key":"B","text":"$-\\tan x$"},{"key":"C","text":"$\\cot x$"},{"key":"D","text":"$-\\sin x$"}],"answer":"B","explanation":"链式法则：$y'=\\frac{1}{\\cos x}\\cdot(-\\sin x)=-\\tan x$。"},
                {"id":"calc_q019","type":"single_choice","question":"$y=xe^x$ 的导数 $y'$ 等于？","options":[{"key":"A","text":"$e^x$"},{"key":"B","text":"$xe^x$"},{"key":"C","text":"$(x+1)e^x$"},{"key":"D","text":"$x^2e^x$"}],"answer":"C","explanation":"乘法法则：$(xe^x)'=1\\cdot e^x+x\\cdot e^x=(x+1)e^x$。"}
              ]
            },
            {
              "id": "calc_kp010",
              "title": "高阶导数",
              "content_type": "markdown",
              "content": "## 高阶导数\n\n$y=f(x)$ 的导数 $f'(x)$ 仍是函数，对其再求导得**二阶导数**：\n\n$$y''=f''(x)=\\frac{d^2y}{dx^2}$$\n\n类似可定义 $n$ 阶导数 $f^{(n)}(x)=\\frac{d^ny}{dx^n}$。\n\n### 常见高阶导数公式\n- $(e^x)^{(n)}=e^x$\n- $(\\sin x)^{(n)}=\\sin(x+\\frac{n\\pi}{2})$\n- $(\\cos x)^{(n)}=\\cos(x+\\frac{n\\pi}{2})$\n- $(x^m)^{(n)}=m(m-1)\\cdots(m-n+1)x^{m-n}$（$n\\leq m$）\n\n### 莱布尼茨公式\n$$(uv)^{(n)}=\\sum_{k=0}^n C_n^k u^{(n-k)}v^{(k)}$$\n\n### 二阶导数的物理意义\n位移 $s(t)$ 的一阶导数为速度，二阶导数为加速度。",
              "key_concepts": ["二阶导数","n阶导数","莱布尼茨公式","加速度"],
              "quizzes": [
                {"id":"calc_q020","type":"single_choice","question":"$y=e^{2x}$ 的二阶导数 $y''$ 等于？","options":[{"key":"A","text":"$e^{2x}$"},{"key":"B","text":"$2e^{2x}$"},{"key":"C","text":"$4e^{2x}$"},{"key":"D","text":"$8e^{2x}$"}],"answer":"C","explanation":"$y'=2e^{2x}$，$y''=4e^{2x}$。通式 $(e^{2x})^{(n)}=2^ne^{2x}$。"}
              ]
            }
          ]
        },
        {
          "id": "calc_sec07",
          "title": "2.3 函数的微分",
          "knowledge_points": [
            {
              "id": "calc_kp011",
              "title": "微分的概念与应用",
              "content_type": "markdown",
              "content": "## 微分的定义\n\n若 $y=f(x)$ 在 $x_0$ 处可导，则：\n\n$$dy=f'(x_0)dx$$\n\n称为函数在 $x_0$ 处的**微分**。$dx=\\Delta x$ 是自变量的微分。\n\n## 几何意义\n$dy$ 是切线的增量，$\\Delta y$ 是曲线的实际增量。当 $|\\Delta x|$ 很小时，$\\Delta y\\approx dy$。\n\n## 可导与可微的关系\n对一元函数：可导 $\\iff$ 可微。\n\n## 一阶微分形式不变性\n无论 $u$ 是自变量还是中间变量，均有 $dy=f'(u)du$。\n\n## 近似计算\n$$f(x_0+\\Delta x)\\approx f(x_0)+f'(x_0)\\Delta x$$",
              "key_concepts": ["微分","可微","形式不变性","近似计算","线性主部"],
              "quizzes": [
                {"id":"calc_q021","type":"single_choice","question":"$y=x^3$ 在 $x=1$ 处的微分 $dy$ 等于？","options":[{"key":"A","text":"$dx$"},{"key":"B","text":"$3dx$"},{"key":"C","text":"$3x^2dx$"},{"key":"D","text":"$6dx$"}],"answer":"B","explanation":"$dy=f'(x)dx=3x^2dx$。在 $x=1$，$dy=3\\cdot 1^2\\cdot dx=3dx$。"},
                {"id":"calc_q022","type":"single_choice","question":"用微分估算 $\\sqrt{4.01}$ 的结果约等于？","options":[{"key":"A","text":"2.000"},{"key":"B","text":"2.005"},{"key":"C","text":"2.0025"},{"key":"D","text":"2.010"}],"answer":"C","explanation":"$f(x)=\\sqrt{x}$，$f'(x)=\\frac{1}{2\\sqrt{x}}$。$f(4.01)\\approx f(4)+f'(4)\\cdot 0.01=2+\\frac{0.01}{4}=2.0025$。"}
              ]
            }
          ]
        }
      ]
    },
    # ===== 第3章: 中值定理与导数应用 (4节, 4知识点, 8题) =====
    {
      "id": "calc_ch03",
      "title": "第三章 中值定理与导数应用",
      "sections": [
        {
          "id": "calc_sec08",
          "title": "3.1 微分中值定理",
          "knowledge_points": [
            {
              "id": "calc_kp012",
              "title": "罗尔定理与拉格朗日中值定理",
              "content_type": "markdown",
              "content": "## 罗尔 (Rolle) 定理\n\n若 $f(x)$ 满足：① 在 $[a,b]$ 上连续；② 在 $(a,b)$ 内可导；③ $f(a)=f(b)$\n\n则 $\\exists\\xi\\in(a,b)$ 使 $f'(\\xi)=0$。\n\n## 拉格朗日 (Lagrange) 中值定理\n\n若 $f(x)$ 在 $[a,b]$ 上连续，在 $(a,b)$ 内可导，则 $\\exists\\xi\\in(a,b)$ 使：\n\n$$f'(\\xi)=\\frac{f(b)-f(a)}{b-a}$$\n\n**几何意义**：曲线上存在一点，该点切线平行于连接端点的弦。\n\n**推论**：① 若区间上 $f'(x)\\equiv 0$，则 $f(x)$ 为常数；② 若 $f'(x)=g'(x)$，则 $f(x)=g(x)+C$。\n\n## 柯西 (Cauchy) 中值定理\n若 $f,g$ 在 $[a,b]$ 连续、$(a,b)$ 可导且 $g'(x)\\neq 0$，则 $\\exists\\xi\\in(a,b)$ 使：\n\n$$\\frac{f'(\xi)}{g'(\xi)}=\\frac{f(b)-f(a)}{g(b)-g(a)}$$",
              "key_concepts": ["罗尔定理","拉格朗日中值定理","柯西中值定理","导数为零则函数为常数"],
              "quizzes": [
                {"id":"calc_q023","type":"single_choice","question":"罗尔定理的条件不包括？","options":[{"key":"A","text":"在 $[a,b]$ 上连续"},{"key":"B","text":"在 $(a,b)$ 内可导"},{"key":"C","text":"$f(a)=f(b)$"},{"key":"D","text":"$f'(a)=f'(b)$"}],"answer":"D","explanation":"罗尔定理三条件：闭区间连续、开区间可导、端点值相等。结论是存在 $\\xi$ 使 $f'(\\xi)=0$。"},
                {"id":"calc_q024","type":"single_choice","question":"$f(x)=x^2$ 在 $[0,2]$ 上满足 Lagrange 定理的 $\\xi$ 值为？","options":[{"key":"A","text":"0"},{"key":"B","text":"1"},{"key":"C","text":"2"},{"key":"D","text":"1.5"}],"answer":"B","explanation":"$f'(x)=2x$，$\\frac{f(2)-f(0)}{2-0}=2$。令 $f'(\\xi)=2\\xi=2$，得 $\\xi=1\\in(0,2)$。"}
              ]
            }
          ]
        },
        {
          "id": "calc_sec09",
          "title": "3.2 洛必达法则",
          "knowledge_points": [
            {
              "id": "calc_kp013",
              "title": "洛必达法则与不定式",
              "content_type": "markdown",
              "content": "## 洛必达 (L'H\\u00f4pital) 法则\n\n### $\\frac{0}{0}$ 型\n若 $\\lim f(x)=\\lim g(x)=0$，且 $\\lim\\frac{f'(x)}{g'(x)}$ 存在（或为 $\\infty$），则：\n\n$$\\lim\\frac{f(x)}{g(x)}=\\lim\\frac{f'(x)}{g'(x)}$$\n\n### $\\frac{\\infty}{\\infty}$ 型\n类似条件下结论同上。\n\n### 可转化为 $\\frac{0}{0}$ 或 $\\frac{\\infty}{\\infty}$ 的类型\n- **$0\\cdot\\infty$ 型**：化为 $\\frac{0}{1/\\infty}$ 或 $\\frac{\\infty}{1/0}$\n- **$\\infty-\\infty$ 型**：通分或有理化\n- **$0^0,\\infty^0,1^{\\infty}$ 型**：取对数化为 $0\\cdot\\infty$ 型\n\n**注意事项**：\n1. 使用前必须验证是否为 $\\frac{0}{0}$ 或 $\\frac{\\infty}{\\infty}$ 型\n2. 每次求导后检查是否仍需（可）继续使用\n3. 结合等价无穷小替换可简化计算",
              "key_concepts": ["0/0型","∞/∞型","可转化不定式","洛必达条件"],
              "quizzes": [
                {"id":"calc_q025","type":"single_choice","question":"$\\lim_{x\\to 0}\\frac{e^x-1}{x}$ 等于？","options":[{"key":"A","text":"0"},{"key":"B","text":"1"},{"key":"C","text":"$e$"},{"key":"D","text":"不存在"}],"answer":"B","explanation":"$\\frac{0}{0}$ 型，洛必达：$\\lim_{x\\to 0}\\frac{(e^x-1)'}{(x)'}=\\lim_{x\\to 0}\\frac{e^x}{1}=1$。"},
                {"id":"calc_q026","type":"single_choice","question":"$\\lim_{x\\to 0^+}x\\ln x$ 等于？","options":[{"key":"A","text":"0"},{"key":"B","text":"1"},{"key":"C","text":"-1"},{"key":"D","text":"不存在"}],"answer":"A","explanation":"$0\\cdot(-\\infty)$ 型，化为 $\\frac{\\ln x}{1/x}$（$\\frac{-\\infty}{\\infty}$）。洛必达：$\\lim_{x\\to 0^+}\\frac{1/x}{-1/x^2}=\\lim_{x\\to 0^+}(-x)=0$。"}
              ]
            }
          ]
        },
        {
          "id": "calc_sec10",
          "title": "3.3 函数的单调性与极值",
          "knowledge_points": [
            {
              "id": "calc_kp014",
              "title": "单调性判别与极值求法",
              "content_type": "markdown",
              "content": "## 单调性判别\n\n设 $f$ 在 $[a,b]$ 连续、$(a,b)$ 可导：\n- $f'(x)>0$ → $f$ 严格递增\n- $f'(x)<0$ → $f$ 严格递减\n\n## 函数的极值\n\n### 必要条件\n若 $f$ 在 $x_0$ 可导且取极值，则 $f'(x_0)=0$（$x_0$ 称为**驻点**）。\n\n注意：驻点不一定是极值点（反例：$y=x^3$ 在 $x=0$）。\n\n### 第一充分条件（看一阶导数变号）\n- 左正右负 → 极大值\n- 左负右正 → 极小值\n- 左右同号 → 非极值\n\n### 第二充分条件（看二阶导数符号）\n设 $f'(x_0)=0$，$f''(x_0)$ 存在：\n- $f''(x_0)<0$ → 极大值\n- $f''(x_0)>0$ → 极小值\n- $f''(x_0)=0$ → 不确定（需用第一充分条件）",
              "key_concepts": ["单调性","驻点","极值必要条件","第一充分条件","第二充分条件"],
              "quizzes": [
                {"id":"calc_q027","type":"single_choice","question":"$f(x)=x^3-3x$ 在 $x=-1$ 处取得？","options":[{"key":"A","text":"极大值"},{"key":"B","text":"极小值"},{"key":"C","text":"非极值"},{"key":"D","text":"无法判断"}],"answer":"A","explanation":"$f'(x)=3x^2-3$，驻点 $x=-1,1$。$f''(x)=6x$，$f''(-1)=-6<0$，故 $x=-1$ 处取极大值 $f(-1)=2$。"},
                {"id":"calc_q028","type":"single_choice","question":"$f'(x_0)=0$ 是 $f(x)$ 在 $x_0$ 取极值的？","options":[{"key":"A","text":"充要条件"},{"key":"B","text":"充分非必要"},{"key":"C","text":"必要非充分"},{"key":"D","text":"既非充分也非必要"}],"answer":"C","explanation":"可导函数极值点必是驻点（必要），但驻点不一定是极值点，如 $y=x^3$ 在 $x=0$（充分性不成立）。"}
              ]
            }
          ]
        },
        {
          "id": "calc_sec11",
          "title": "3.4 曲线的凹凸性与渐近线",
          "knowledge_points": [
            {
              "id": "calc_kp015",
              "title": "凹凸性、拐点与渐近线",
              "content_type": "markdown",
              "content": "## 凹凸性\n\n设 $f$ 具有二阶导数：\n- $f''(x)>0$ → 曲线是**凹的**（下凸，碗口向上）\n- $f''(x)<0$ → 曲线是**凸的**（上凸，碗口向下）\n\n## 拐点\n曲线凹凸性改变的点称为**拐点**。若 $(x_0,f(x_0))$ 是拐点且 $f''(x_0)$ 存在，则 $f''(x_0)=0$。\n\n判别：若 $f''(x)$ 在 $x_0$ 两侧变号，则 $(x_0,f(x_0))$ 是拐点。\n\n## 渐近线\n1. **水平渐近线**：若 $\\lim_{x\\to\\infty}f(x)=A$，则 $y=A$\n2. **垂直渐近线**：若 $\\lim_{x\\to x_0}f(x)=\\infty$，则 $x=x_0$\n3. **斜渐近线**：若 $\\lim_{x\\to\\infty}\\frac{f(x)}{x}=k$，$\\lim_{x\\to\\infty}[f(x)-kx]=b$，则 $y=kx+b$",
              "key_concepts": ["凹","凸","拐点","水平渐近线","垂直渐近线","斜渐近线"],
              "quizzes": [
                {"id":"calc_q029","type":"single_choice","question":"$y=x^3$ 的拐点是？","options":[{"key":"A","text":"$(0,0)$"},{"key":"B","text":"$(1,1)$"},{"key":"C","text":"$(-1,-1)$"},{"key":"D","text":"没有拐点"}],"answer":"A","explanation":"$y''=6x$。$x<0$ 时 $y''<0$（凸）；$x>0$ 时 $y''>0$（凹）。在 $x=0$ 处变号，$(0,0)$ 是拐点。"},
                {"id":"calc_q030","type":"single_choice","question":"$f''(x)>0$ 在 $(a,b)$ 内成立，说明曲线在该区间内？","options":[{"key":"A","text":"递增"},{"key":"B","text":"递减"},{"key":"C","text":"凹的（下凸）"},{"key":"D","text":"凸的（上凸）"}],"answer":"C","explanation":"$f''(x)>0$ → 凹的（下凸）。单调性由 $f'(x)$ 的符号决定。$f''(x)<0$ → 凸的（上凸）。"}
              ]
            }
          ]
        }
      ]
    }
  ]
}

# 保存
out_path = "E:/.Claude Code Project/3.知识学习APP_20260528/knowledge_app/assets/content/math_calculus.json"
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(content, f, ensure_ascii=False, indent=2)

# 统计
kp_count = sum(len(kp) for ch in content['chapters'] for sec in ch['sections'] for kp in [sec['knowledge_points']])
quiz_count = sum(len(kp['quizzes']) for ch in content['chapters'] for sec in ch['sections'] for kp in sec['knowledge_points'])
size = round(os.path.getsize(out_path) / 1024)

print(f"Generated {out_path}")
print(f"  Chapters: {len(content['chapters'])}")
print(f"  Sections: {sum(len(ch['sections']) for ch in content['chapters'])}")
print(f"  Knowledge Points: {kp_count}")
print(f"  Quizzes: {quiz_count}")
print(f"  File size: {size} KB")
