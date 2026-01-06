import streamlit as st
import streamlit.components.v1 as components

# 設定頁面資訊
st.set_page_config(
    page_title="DSE 中國歷史成績模擬器",
    page_icon="📚",
    layout="wide"
)

# 讀取或直接嵌入 HTML 內容
html_code = """
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8">
  <title>DSE 中國歷史 · 成績模擬與溫習規劃</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    * { box-sizing: border-box; }
    :root { color-scheme: light; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", Roboto, "Noto Sans TC", sans-serif;
      margin: 0;
      padding: 0;
      background: radial-gradient(circle at top, #eef2ff 0, #f5f5f7 40%, #f9fafb 100%);
      color: #111827;
      overflow-x: hidden;
    }
    .container {
      max-width: 980px;
      margin: 10px auto;
      padding: 0 16px;
    }
    /* 以下省略部分重複的 CSS 以節省空間，請確保使用你提供的完整 CSS */
    .page-header { margin-bottom: 18px; }
    .title-row { display: flex; justify-content: space-between; align-items: center; gap: 12px; }
    h1 { font-size: 26px; font-weight: 800; letter-spacing: -0.03em; margin: 0; }
    .chip { padding: 4px 10px; border-radius: 999px; font-size: 12px; background: rgba(37,99,235,0.08); color: #1d4ed8; font-weight: 600; display: inline-flex; align-items: center; gap: 6px; }
    .chip-dot { width: 7px; height: 7px; border-radius: 999px; background: #22c55e; }
    .subtitle { margin-top: 6px; color: #4b5563; font-size: 13px; line-height: 1.6; }
    .card { background: rgba(255,255,255,0.92); backdrop-filter: blur(20px); border-radius: 22px; padding: 20px 18px; box-shadow: 0 24px 60px rgba(0,0,0,0.04), 0 0 0 1px rgba(148,163,184,0.18); margin-bottom: 18px; }
    .card-header { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 10px; gap: 8px; }
    h2 { font-size: 18px; margin: 0; }
    .card-caption { font-size: 12px; color: #6b7280; }
    .section-label { font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: #9ca3af; margin-bottom: 8px; }
    .inputs-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; }
    .input-group { background: #f9fafb; border-radius: 16px; padding: 10px 12px 12px; border: 1px solid #e5e7eb; }
    .input-label-row { display: flex; justify-content: space-between; align-items: center; gap: 6px; margin-bottom: 4px; }
    label { font-weight: 600; font-size: 13px; color: #111827; }
    .badge { padding: 3px 8px; border-radius: 999px; font-size: 11px; background: #eff6ff; color: #1d4ed8; white-space: nowrap; }
    .hint { font-size: 11px; color: #6b7280; margin-top: 4px; line-height: 1.5; }
    input[type="number"] { width: 100%; margin-top: 4px; padding: 10px 11px; font-size: 16px; border-radius: 12px; border: 1px solid #e5e7eb; outline: none; background: #ffffff; text-align: right; }
    .paper-tag { display: inline-flex; gap: 6px; align-items: center; font-size: 11px; color: #4b5563; }
    .pill { padding: 2px 8px; border-radius: 999px; background: #e5e7eb; font-size: 11px; }
    button { width: 100%; padding: 13px; font-size: 16px; font-weight: 700; border: none; border-radius: 999px; background: linear-gradient(135deg, #2563eb, #4f46e5); color: #fff; cursor: pointer; margin-top: 6px; box-shadow: 0 14px 28px rgba(37,99,235,0.35); transition: all 0.12s; }
    button:hover { transform: translateY(-1px); box-shadow: 0 18px 32px rgba(37,99,235,0.4); }
    .error { color: #b91c1c; font-size: 12px; margin-top: 6px; }
    .result-section { display: none; }
    .result-main { display: flex; flex-wrap: wrap; align-items: baseline; gap: 10px; margin-bottom: 4px; }
    .level { font-size: 30px; font-weight: 800; letter-spacing: -0.04em; color: #111827; }
    .percent { font-size: 18px; color: #4b5563; }
    .tagline { font-size: 13px; color: #6b7280; margin-top: 4px; }
    .warning { margin-top: 6px; font-size: 13px; color: #b91c1c; font-weight: 600; }
    table { width: 100%; border-collapse: collapse; font-size: 12px; margin-top: 6px; }
    th, td { border: 1px solid #e5e7eb; padding: 5px 6px; text-align: center; }
    th { background: #f3f4f6; font-weight: 600; }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 10px; margin-top: 10px; }
    .small-card { border-radius: 16px; border: 1px solid #e5e7eb; padding: 10px 12px; background: #f9fafb; font-size: 12px; line-height: 1.5; }
    .small-card h3 { font-size: 13px; margin: 0 0 4px; }
    ul { padding-left: 18px; margin: 4px 0; }
    li { margin-bottom: 4px; }
    .subtle { font-size: 11px; color: #9ca3af; margin-top: 4px; }
    .chips-row { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 4px; font-size: 11px; }
    .mini-chip { padding: 3px 8px; border-radius: 999px; background: #e5e7eb; color: #4b5563; }
    @media (max-width: 640px) { h1 { font-size: 22px; } }
  </style>
</head>
<body>
<div class="container">
  <div class="page-header">
    <div class="title-row">
      <h1>DSE 中國歷史 · 成績模擬與溫習規劃</h1>
      <div class="chip"><span class="chip-dot"></span> For S6 Students</div>
    </div>
    <p class="subtitle">輸入你在各部分的預計分數（模擬卷、校內試或自我估算）。系統會自動計算等級並提供溫習建議。</p>
  </div>

  <div class="card">
    <div class="card-header">
      <h2>分數輸入</h2>
      <div class="paper-tag"><span class="pill">Paper 1</span><span class="pill">Paper 2</span></div>
    </div>
    <div class="section-label">Paper 1 · 必答題 (31%)</div>
    <div class="inputs-grid">
      <div class="input-group">
        <div class="input-label-row"><label for="p1AComp">甲部 必答題</label><span class="badge">20 分</span></div>
        <input id="p1AComp" type="number" min="0" max="20" placeholder="0 - 20">
      </div>
      <div class="input-group">
        <div class="input-label-row"><label for="p1BComp">乙部 必答題</label><span class="badge">20 分</span></div>
        <input id="p1BComp" type="number" min="0" max="20" placeholder="0 - 20">
      </div>
    </div>

    <div class="section-label" style="margin-top: 14px;">Paper 1 · 選答題 (39%)</div>
    <div class="inputs-grid">
      <div class="input-group">
        <div class="input-label-row"><label for="p1AElect">甲部 選答題</label><span class="badge">25 分</span></div>
        <input id="p1AElect" type="number" min="0" max="25" placeholder="0 - 25">
      </div>
      <div class="input-group">
        <div class="input-label-row"><label for="p1BElect">乙部 選答題</label><span class="badge">25 分</span></div>
        <input id="p1BElect" type="number" min="0" max="25" placeholder="0 - 25">
      </div>
    </div>

    <div class="section-label" style="margin-top: 14px;">Paper 2 · 歷史專題 (30%)</div>
    <div class="inputs-grid">
      <div class="input-group"><label>黃河流域</label><input id="p2Yellow" type="number" min="0" max="25" placeholder="0-25"></div>
      <div class="input-group"><label>長江流域</label><input id="p2Yangtze" type="number" min="0" max="25" placeholder="0-25"></div>
      <div class="input-group"><label>珠江流域</label><input id="p2Pearl" type="number" min="0" max="25" placeholder="0-25"></div>
    </div>
    <div id="error" class="error"></div>
    <button id="calcBtn">計算成績與溫習建議</button>
  </div>

  <div id="result" class="card result-section">
    <div class="result-main">
      <div class="level" id="levelText">–</div>
      <div class="percent" id="percentText"></div>
    </div>
    <div class="tagline" id="taglineText"></div>
    <div class="warning" id="warningText"></div>
    <div class="grid">
      <div class="small-card"><h3>得分佔比</h3><table><thead><tr><th>部分</th><th>折算%</th></tr></thead><tbody id="partTableBody"></tbody></table></div>
      <div class="small-card"><h3>升級目標</h3><div id="nextLevelBlock"></div></div>
    </div>
    <div class="small-card" style="margin-top:10px;"><h3>溫習建議</h3><ul id="studyTips"></ul></div>
  </div>
</div>

<script>
  // 這裡放入你原本 HTML 中的完整 JavaScript 邏輯
  const cutoffs = [
    { level: "5**", score: 82 }, { level: "5*", score: 74 }, { level: "5", score: 70 },
    { level: "4", score: 60 }, { level: "3", score: 50 }, { level: "2", score: 30 }, { level: "1", score: 1 }
  ];
  function getLevel(p) { for (const c of cutoffs) { if (p >= c.score) return c.level; } return "U"; }
  function getNextLevelInfo(p) { 
    const sorted = [...cutoffs].sort((a, b) => a.score - b.score);
    for (const c of sorted) { if (p < c.score) return { targetLevel: c.level, targetScore: c.score, diff: c.score - p }; }
    return null;
  }

  document.getElementById("calcBtn").addEventListener("click", function() {
    const p1A = parseFloat(document.getElementById("p1AComp").value) || 0;
    const p1B = parseFloat(document.getElementById("p1BComp").value) || 0;
    const p1AE = parseFloat(document.getElementById("p1AElect").value) || 0;
    const p1BE = parseFloat(document.getElementById("p1BElect").value) || 0;
    const p2Y = parseFloat(document.getElementById("p2Yellow").value) || 0;
    const p2Z = parseFloat(document.getElementById("p2Yangtze").value) || 0;
    const p2P = parseFloat(document.getElementById("p2Pearl").value) || 0;

    const p1Percent = (p1A/20*15.5) + (p1B/20*15.5) + (p1AE/25*19.5) + (p1BE/25*19.5);
    const p2BestTwo = [p2Y, p2Z, p2P].sort((a,b)=>b-a).slice(0,2).reduce((a,b)=>a+b, 0);
    const p2Percent = (p2BestTwo/50*30);
    const total = Math.round((p1Percent + p2Percent) * 10) / 10;
    
    document.getElementById("levelText").textContent = "等級：" + getLevel(total);
    document.getElementById("percentText").textContent = total + " %";
    document.getElementById("result").style.display = "block";
    
    const next = getNextLevelInfo(total);
    document.getElementById("nextLevelBlock").innerHTML = next ? `距離 ${next.targetLevel} 還差 ${Math.round(next.diff*10)/10}%` : "已達最高等級";
    
    const tips = document.getElementById("studyTips");
    tips.innerHTML = "<li>加強卷一資料扣連技巧</li><li>整理卷二專題論證框架</li>";
    
    if (total < 50) {
        document.getElementById("warningText").textContent = "⚠️ 建議聯絡郭Sir（97701850）獲取專業指導。";
    } else {
        document.getElementById("warningText").textContent = "";
    }
    
    const tbody = document.getElementById("partTableBody");
    tbody.innerHTML = `<tr><td>卷一</td><td>\${p1Percent.toFixed(1)}%</td></tr><tr><td>卷二</td><td>\${p2Percent.toFixed(1)}%</td></tr>`;
  });
</script>
</body>
</html>
"""

# 使用 Streamlit HTML 元件渲染
# height 可以根據內容長度調整
components.html(html_code, height=1200, scrolling=True)