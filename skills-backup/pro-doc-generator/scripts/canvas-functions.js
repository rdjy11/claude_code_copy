// Canvas 泳道图核心绘图函数
// 使用方式：复制到 HTML <script> 标签中，配合 drawSwimlane() 主函数使用

// 圆角矩形路径
function roundRect(ctx, x, y, w, h, r) {
  ctx.beginPath();
  ctx.moveTo(x+r, y); ctx.lineTo(x+w-r, y);
  ctx.quadraticCurveTo(x+w, y, x+w, y+r); ctx.lineTo(x+w, y+h-r);
  ctx.quadraticCurveTo(x+w, y+h, x+w-r, y+h); ctx.lineTo(x+r, y+h);
  ctx.quadraticCurveTo(x, y+h, x, y+h-r); ctx.lineTo(x, y+r);
  ctx.quadraticCurveTo(x, y, x+r, y); ctx.closePath();
}

// 矩形节点（带投影 + 多行文字）
function drawBox(ctx, x, y, w, h, text, opts) {
  const { fill, stroke, radius = 8, bold = false } = opts;
  ctx.save(); ctx.shadowColor = 'rgba(0,0,0,0.08)';
  ctx.shadowBlur = 8; ctx.shadowOffsetY = 2;
  ctx.fillStyle = fill; roundRect(ctx, x, y, w, h, radius); ctx.fill();
  ctx.restore();
  ctx.strokeStyle = stroke; ctx.lineWidth = 2;
  roundRect(ctx, x, y, w, h, radius); ctx.stroke();
  // 多行居中文字
  ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  text.split('\n').forEach((t, i, arr) => {
    ctx.font = (i===0 && bold) ? 'bold 12px "PingFang SC", sans-serif'
                                : '12px "PingFang SC", sans-serif';
    ctx.fillStyle = (i===0 && bold) ? stroke : '#444';
    ctx.fillText(t, x+w/2, y+h/2 + (i-(arr.length-1)/2)*17);
  });
  return { x, y, w, h, cx: x+w/2, cy: y+h/2, l: x, r: x+w, t: y, b: y+h };
}

// 菱形节点（KCP）
function drawDiamond(ctx, cx, cy, rw, rh, text, opts) {
  const { fill = '#fce4ec', stroke = '#e91e63' } = opts;
  ctx.save(); ctx.shadowColor = 'rgba(0,0,0,0.08)';
  ctx.shadowBlur = 8; ctx.shadowOffsetY = 2;
  ctx.fillStyle = fill;
  ctx.beginPath();
  ctx.moveTo(cx, cy-rh); ctx.lineTo(cx+rw, cy);
  ctx.lineTo(cx, cy+rh); ctx.lineTo(cx-rw, cy);
  ctx.closePath(); ctx.fill(); ctx.restore();
  ctx.strokeStyle = stroke; ctx.lineWidth = 2.2;
  ctx.beginPath();
  ctx.moveTo(cx, cy-rh); ctx.lineTo(cx+rw, cy);
  ctx.lineTo(cx, cy+rh); ctx.lineTo(cx-rw, cy);
  ctx.closePath(); ctx.stroke();
  // 居中文字
  text.split('\n').forEach((t, i, arr) => {
    ctx.font = i===0 ? 'bold 11px "PingFang SC", sans-serif'
                      : '11px "PingFang SC", sans-serif';
    ctx.fillStyle = i===0 ? stroke : '#555';
    ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.fillText(t, cx, cy + (i-(arr.length-1)/2)*15);
  });
  return { cx, cy, rw, rh, l: cx-rw, r: cx+rw, t: cy-rh, b: cy+rh };
}

// 折线箭头（支持多段折点 + 虚线）
function arrowLine(ctx, pts, opts) {
  const { color = '#666', dash = false, width = 1.8 } = opts;
  ctx.strokeStyle = color; ctx.lineWidth = width;
  ctx.setLineDash(dash ? [8, 5] : []);
  ctx.beginPath(); ctx.moveTo(pts[0][0], pts[0][1]);
  for (let i = 1; i < pts.length; i++) ctx.lineTo(pts[i][0], pts[i][1]);
  ctx.stroke(); ctx.setLineDash([]);
  // 实心三角箭头
  const p = pts[pts.length-2], q = pts[pts.length-1];
  const a = Math.atan2(q[1]-p[1], q[0]-p[0]), L = 9;
  ctx.fillStyle = color; ctx.beginPath();
  ctx.moveTo(q[0], q[1]);
  ctx.lineTo(q[0]-L*Math.cos(a-0.35), q[1]-L*Math.sin(a-0.35));
  ctx.lineTo(q[0]-L*Math.cos(a+0.35), q[1]-L*Math.sin(a+0.35));
  ctx.closePath(); ctx.fill();
}

// 连线标签
function arrowLabel(ctx, pts, text, opts) {
  const { color = '#666', above = true } = opts;
  const mid = pts.length === 2
    ? [(pts[0][0]+pts[1][0])/2, (pts[0][1]+pts[1][1])/2]
    : pts[1];
  ctx.font = 'bold 11px "PingFang SC", sans-serif';
  ctx.fillStyle = color; ctx.textAlign = 'center';
  ctx.textBaseline = above ? 'bottom' : 'top';
  ctx.fillText(text, mid[0], mid[1] + (above ? -5 : 5));
}
