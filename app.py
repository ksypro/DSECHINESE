import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="DSE 中史模擬器", layout="wide")

html_code = """
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    /* 核心 UI 樣式 - 完全對照截圖 */
    body { background-color: #f0f2f5; font-family: -apple-system, BlinkMacSystemFont, sans-serif; padding: 20px; display: flex; justify-content: center; }
    .card { background: white; border-radius: 24px; padding: 40px; box-shadow: 0 4px 24px rgba(0,0,0,0.06); max-width: 950px; width: 100%; }
    h1 { font-size: 28px; font-weight: 800; color: #1d1d1f; margin: 0; }
    .subtitle { color: #6e6e73; font-size: 14px; margin: 10px 0 30px; }
    .section-title { font-size: 13px; font-weight: 700; color: #86868b; text-transform: uppercase; margin: 25px 0 10px 5px; }
    
    .inputs-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }
    .p2-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; }
    .input-box { border: 1px solid #d2d2d7; border-radius: 16px; padding: 18px; position: relative; background: #fbfbfd; }
    .input-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
    .input-header label { font-size: 15px; font-weight: 700; }
    .weight-tag { font-size: 12px; color: #0066cc; background: #f0f7ff; padding: 2px 8px; border-radius: 4px; }
    .real-input { width: 100%; border: none; font-size: 24px; font-weight: 500; outline: none; background: transparent; }
    .range-hint { position: absolute; right: 18px; bottom: 18px; color: #86868b; font-size: 18px; }

    .calc-btn { width: 100%; background: #5e5ce6; color: white; border: none; border-radius: 20px; padding: 20px; font-size: 18px; font-weight: 700; cursor: pointer; margin-top: 30px; }
    
    /* 結果區樣式 */
    .result-section { display: none; margin-top: 40px; }
    .level-row { display: flex; align-items: baseline; gap: 15px; }
    .level-big { font-size: 72px; font-weight: 800; color: #5e5ce6; margin: 0; }
    .percent-big { font-size: 32px; font-weight: 600; color: #1d1d1f; }
    .tagline { font-size: 16px; color: #1d1d1f; margin: 15px 0; }
    .warn-box { background: #fff2f2; border: 1px solid #ffcfcf; border-radius: 12px; padding: 15px; color: #d70015; font-weight: 600; display: flex; align-items: center; gap: 10px; margin-bottom: 30px; }

    /* 建議卡片樣式 - 對齊截圖裝飾 */
    .advice-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 25px; }
    .advice-card { background: #f8f9fa; border-radius: 20px; padding: 30px; border: 1px solid #e5e5e5; position: relative; }
    .advice-card::before { content: ""; position: absolute; left: 20px; top: 30px; bottom: 30px; width: 4px; border-radius: 2px; }
    .strategy-card::before { background: #5e5ce6; }
    .study-card::before { background: #34c759; }
    
    .advice-card h3 { margin: 0 0 20px 15px; font-size: 18px; display: flex; align-items: center; gap: 10px; }
    .strategy-content, .study-tips { margin-left: 15px; font-size: 14.5px; line-height: 1.8; color: #3a3a3c; }
    .strategy-content strong { color: #0071e3; }
    .subtle { font-size: 12px; color: #86868b; margin-top: 15px; border-top: 1px solid #ddd; padding-top: 10px; }
    
    @media (max-width: 600px) { .inputs-grid, .p2-grid, .advice-grid { grid-template-columns: 1fr; } }
  </style>
</head>
<body>
<div class="card">
  <h1>DSE 中國歷史 · 成績模擬與溫習規劃</h1>
  <p class="subtitle">輸入分數後，系統將根據比重計算全科 CP 值，並提供針對性的搶分建議。</p>

  <div class="section-title">PAPER 1 · 必答題 (31%)</div>
  <div class="inputs-grid">
    <div class="input-box"><div class="input-header"><label>甲部 必答</label><span class="weight-tag">全科 15.5%</span></div><input type="number" id="p1a" class="real-input" value="0"><span class="range-hint">/ 20</span></div>
    <div class="input-box"><div class="input-header"><label>乙部 必答</label><span class="weight-tag">全科 15.5%</span></div><input type="number" id="p1b" class="real-input" value="0"><span class="range-hint">/ 20</span></div>
  </div>

  <div class="section-title">PAPER 1 · 選答題 (39%)</div>
  <div class="inputs-grid">
    <div class="input-box"><div class="input-header"><label>甲部 選答</label><span class="weight-tag">全科 19.5%</span></div><input type="number" id="p1ae" class="real-input" value="0"><span class="range-hint">/ 25</span></div>
    <div class="input-box"><div class="input-header"><label>乙部 選答</label><span class="weight-tag">全科 19.5%</span></div><input type="number" id="p1be" class="real-input" value="0"><span class="range-hint">/ 25</span></div>
  </div>

  <div class="section-title">PAPER 2 · 歷史專題 (30%)</div>
  <div class="p2-grid">
    <div class="input-box"><label>專題 1</label><input type="number" id="p2_1" class="real-input" value="0"><span class="range-hint">/ 25</span></div>
    <div class="input-box"><label>專題 2</label><input type="number" id="p2_2" class="real-input" value="0"><span class="range-hint">/ 25</span></div>
    <div class="input-box"><label>專題 3</label><input type="number" id="p2_3" class="real-input" value="0"><span class="range-hint">/ 25</span></div>
  </div>

  <button class="calc-btn" id="calcBtn">計算模擬成績與搶分策略</button>

  <div id="result" class="result-section">
    <div class="level-row"><div id="resLvl" class="level-big"></div><div id="resPerc" class="percent-big"></div></div>
    <p id="tagline" class="tagline"></p>
    <div id="warnBox"></div>

    <div class="advice-grid">
      <div class="advice-card strategy-card">
        <h3>🎯 重點推分策略</h3>
        <div id="valAdvice" class="strategy-content"></div>
      </div>
      <div class="advice-card study-card">
        <h3>📚 溫習方向建議</h3>
        <div id="studyTips" class="study-tips"></div>
      </div>
    </div>
  </div>
</div>

<script>
document.getElementById("calcBtn").addEventListener("click", function() {
  const v = (id) => parseFloat(document.getElementById(id).value) || 0;
  
  // 1. 加權計算
  const p1a = v("p1a"), p1b = v("p1b"), p1ae = v("p1ae"), p1be = v("p1be");
  const p2Raw = [v("p2_1"), v("p2_2"), v("p2_3")].sort((a,b)=>b-a);
  const p2Best = p2Raw[0] + p2Raw[1];

  const p1ap = (p1a/20)*15.5, p1bp = (p1b/20)*15.5, p1aep = (p1ae/25)*19.5, p1bep = (p1be/25)*19.5, p2p = (p2Best/50)*30;
  const total = Math.round((p1ap + p1bp + p1aep + p1bep + p2p) * 10) / 10;

  // 2. 等級與 Tagline
  let level = "U", tagline = "";
  if(total>=82){ level="5**"; tagline="整體表現頂尖，卷一維持命中率，卷二可深化史學觀點。"; }
  else if(total>=74){ level="5*"; tagline="高分段考生，需收窄粗心失分並加強卷二論述層次感。"; }
  else if(total>=70){ level="5"; tagline="中上水平，穩守卷一基礎，再用卷二拉開差距。"; }
  else if(total>=60){ level="4"; tagline="已穩定合格，確保卷一不失分，再挑戰卷二深度題。"; }
  else if(total>=50){ level="3"; tagline="有一定根基，需鞏固史實結構，成績有望再上一級。"; }
  else { level="2/U"; tagline="目前需要重建大事因果關係，配合簡單資料題技巧，慢慢累積分數。"; }

  document.getElementById("resLvl").innerText = level;
  document.getElementById("resPerc").innerText = total + "%";
  document.getElementById("tagline").innerText = tagline;
  document.getElementById("result").style.display = "block";

  // 3. 郭Sir 聯絡提醒
  const warn = document.getElementById("warnBox");
  if (total < 50) {
    warn.innerHTML = `<div class="warn-box">⚠️ 距離目標尚有距離。建議聯絡郭Sir (97701850) 重新制定搶分進度。</div>`;
  } else { warn.innerHTML = ""; }

  // 4. 重點推分策略 (補完邏輯)
  const parts = [
    { name: "卷一 甲部", raw: p1a+p1ae, max: 45, weight: 35 },
    { name: "卷一 乙部", raw: p1b+p1be, max: 45, weight: 35 },
    { name: "卷二 歷史專題", raw: p2Best, max: 50, weight: 30 }
  ];
  const sorted = parts.map(p => ({
    name: p.name,
    cp: p.weight/p.max,
    rem: p.max - p.raw
  })).sort((a,b) => (b.rem*b.cp) - (a.rem*a.cp));

  const best = sorted[0];
  const aPot = ((20-p1a)*0.775) + ((25-p1ae)*0.78);
  const bPot = ((20-p1b)*0.775) + ((25-p1be)*0.78);
  let betterAB = aPot > bPot ? "「甲部」的提升空間較多，可優先整理古代史政策線索。" : "「乙部」的提升空間較多，可先鞏固近現代中國史。";

  document.getElementById("valAdvice").innerHTML = `
    <p>綜合比重與尚可追回的分數後：</p>
    <p>短期內較適合作為重點推分的是：<strong>${best.name}</strong><br>
    · 每增 1 分 ≈ 全科 <strong>${best.cp.toFixed(2)}%</strong><br>
    · 理論上尚餘 <strong>${best.rem.toFixed(1)} 分</strong> 可爭取</p>
    <p style="margin-top:15px;">${betterAB}</p>
    <div class="subtle">卷一必答是穩定的基礎，卷二則是衝擊 5** 的關鍵分析所在。</div>
  `;

  // 5. 溫習方向建議 (補完文字)
  document.getElementById("studyTips").innerHTML = `
    <ul style="margin:0; padding-left:0; list-style:none;">
      <li style="margin-bottom:12px;">📍 <b>整體方針：</b>中史卷考三方面：資料價值與限制、分析比較能力、史實熟悉度。</li>
      <li style="margin-bottom:12px;">📍 <b>建立框架：</b>先從「畫大地圖」開始：為甲部和乙部分別整理簡單時間線。</li>
      <li style="margin-bottom:12px;">📍 <b>答題技巧：</b>卷一資料題練習「先捉重點句，再用自己話解釋」。</li>
      <li>📍 <b>實戰練習：</b>開始接觸 Marking Scheme，用螢光筆標出常見關鍵字眼，建立答題語感。</li>
    </ul>
  `;

  window.scrollTo({ top: document.getElementById("result").offsetTop, behavior: 'smooth' });
});
</script>
</body>
</html>
"""

components.html(html_code, height=1400, scrolling=True)
