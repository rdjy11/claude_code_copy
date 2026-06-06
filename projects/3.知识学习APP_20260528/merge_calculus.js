// 合并微积分 JSON 三部分（避免 PowerShell ConvertTo-Json 的数据损坏 bug）
const fs = require('fs');

function readJson(path) {
  let raw = fs.readFileSync(path, 'utf8');
  if (raw.charCodeAt(0) === 0xFEFF) raw = raw.slice(1); // strip BOM
  return JSON.parse(raw);
}

const baseDir = 'E:/.Claude Code Project/3.知识学习APP_20260528';

// Read all three correct parts
const ch13 = readJson(`${baseDir}/calc_ch13_fixed.json`);
const ch45 = readJson(`${baseDir}/calc_ch45.json`);
const ch68 = readJson(`${baseDir}/calc_ch68.json`);

// Merge chapters into a Course object
const course = {
  course_id: "calculus",
  course_name: "微积分",
  subject_id: "math",
  structure_type: "hierarchical",
  chapters: [...ch13, ...ch45, ...ch68]
};

// Count stats
let kpCount = 0, quizCount = 0;
for (const ch of course.chapters) {
  for (const sec of ch.sections) {
    kpCount += sec.knowledge_points.length;
    for (const kp of sec.knowledge_points) {
      quizCount += kp.quizzes.length;
      // Verify each quiz has required fields
      for (const q of kp.quizzes) {
        if (!q.id || !q.question || !q.options || !q.answer) {
          console.log(`WARNING: Corrupted quiz in ${kp.id}:`, JSON.stringify(q).slice(0, 80));
        }
      }
    }
  }
}

// Save
const outPath = `${baseDir}/knowledge_app/assets/content/math_calculus.json`;
fs.writeFileSync(outPath, JSON.stringify(course, null, 2), 'utf8');
const size = Math.round(fs.statSync(outPath).size / 1024);

console.log(`Merged: ${course.chapters.length} chapters, ${kpCount} KPs, ${quizCount} quizzes, ${size} KB`);
