import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="DSE 中史成績模擬器", layout="wide")

# 這裡的 HTML 包含了所有 CSS 樣式、計算邏輯與補全的文字內容
html_code = """
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    /* UI 介面設定 (對標 Apple 風格) */
    body {
      background-color: #f0f2f5;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      margin: 0; padding: 40px 20px; display: flex; justify-content: center;
    }
    .main-container { max-width: 1000px; width: 100%; }
    .card {
      background: #ffffff; border-radius: 24px; padding: 40px;
      box-shadow: 0 4px 24px rgba(0, 0, 0, 0.06);
    }
    h1 { font-size: 28px; font-weight: 800; margin: 0; color: #1d1d1f; }
    .subtitle { color: #6e6e73; font-size: 14px; margin: 10px 0 30px 0; line-height: 1.5; }
    
    /* 輸入框 Grid 佈局 */
    .section-title { font-size: 13px; font-weight: 700; color: #86868b; text-transform: uppercase; margin: 25px 0 10px 5px; }
    .inputs-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }
    .p2-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; }

    .input-box {
      border: 1px solid #d2d2d7; border-radius: 16px; padding: 18px;
      position: relative; background: #fbfbfd; transition: all 0.2s;
    }
    .input-box:focus-within { border-color: #0066cc; box-shadow: 0 0 0 4px rgba(0, 102, 204, 0.1); }
    .input-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
    .input-header label { font-size: 15px; font-weight: 700; }
    .weight-tag { font-size: 12px; color: #0066cc; background: #f0f7ff; padding: 2px 8px; border-radius: 4px; }
    
    .real-input {
      width: 100%; border: none; font-size: 24px; font-weight: 500;
      outline: none; background: transparent;
    }
    .range-hint { position: absolute; right: 18px; bottom: 18px; color: #86868b; font-size: 16px; }

    /* 按鈕樣式 */
    .calc-btn {
      width: 100%; background: linear-gradient(135deg, #5e5ce6 0%, #4644d1 100%);
      color: white; border: none; border-radius: 20px; padding: 20px;
      font-size: 18px; font-weight: 700; cursor: pointer; margin-top: 30px;
    }

    /* 結果區樣式 */
    .result-section { display: none; margin-top: 40px; border-top: 1px solid #e5e5e5; padding-top: 30px; }
    .level-row { display: flex; align-items: baseline; gap: 15px; }
    .level-big { font-size: 64px; font-weight: 800; color: #5e5ce6; margin: 0; }
    .percent-big { font-size: 28px; font-weight: 600; color: #1d1d1f; }
    .advice-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 25px; }
    .advice-card { background: #f5f5f7; border-radius: 18px; padding: 25px; border: 1px solid #d2d2d7; }
    .advice-card h3 { margin-top: 0; font-size: 17px; border-left: 4px solid #5e5ce6; padding-left: 12px; }
    .strategy-text { font-size: 14.5px; line-height: 1.8; color: #3a3a3c; }
    .strategy-text strong { color: #0071e3; }
    hr { border: 0; border-top: 1px solid #d2d2d7; margin: 15px 0; }

    @media (max-width: 600px) { .inputs-grid, .p2-grid, .advice-grid { grid-template-columns: 1fr; } }
  </style>
</head>
<body>
<div class="main-container">
  <div class="card">
    <h1>DSE 中國歷史 · 成績模擬與溫習規劃</h1>
    <p class="subtitle">輸入預算分數，系統將計算全科比重與 CP 值，並提供針對性的搶分建議。</p>

    <div class="section-title">PAPER 1 · 必答題 (31%)</div>
    <div class="inputs-grid">
      <div class="input-box">
        <div class="input-header"><label>甲部 必答</label><span class="weight-tag">全科 15.5%</span></div>
        <input type="number" id="p1A" class="real-input" value="0">
        <span class="range-hint">/ 20</span>
      </div>
      <div class="input-box">
        <div class="input-header"><label>乙部 必答</label><span class="weight-tag">全科 15.5%</span></div>
        <input type="number" id="p1B" class="real-input" value="0">
        <span class="range-hint">/ 20</span>
      </div>
    </div>

    <div class="section-title">PAPER 1 · 選答題 (39%)</div>
    <div class="inputs-grid">
      <div class="input-box">
        <div class="input-header"><label>甲部 選答</label><span class="weight-tag">全科 19.5%</span></div>
        <input type="number" id="p1AE" class="real-input" value="0">
        <span class="range-hint">/ 25</span>
      </div>
      <div class="input-box">
        <div class="input-header"><label>乙部 選答</label><span class="weight-tag">全科 19.5%</span></div>
        <input type="number" id="p1BE" class="real-input" value="0">
        <span class="range-hint">/ 25</span>
      </div>
    </div>

    <div class="section-title">PAPER 2 · 歷史專題 (30%)</div>
    <div class="p2-grid">
      <div class="input-box"><label>專題 1</label><input type="number" id="p2_1" class="real-input" value="0"><span class="range-hint">/ 25</span></div>
      <div class="input-box"><label>專題 2</label><input type="number" id="p2_2" class="real-input" value="0"><span class="range-hint">/ 25</span></div>
      <div class="input-box"><label>專題 3</label><input type="number" id="p2_3" class="real-input" value="0"><span class="range-hint">/ 25</span></div>
    </div>

    <button class="calc-btn" id="calcBtn">計算模擬成績與搶分策略</button>

    <div id="result" class="result-section">
      <div class="level-row">
        <div id="resLvl" class="level-big"></div>
        <div id="resPerc" class="percent-big"></div>
      </div>
      <p id="tagline" style="font-size: 16px; color: #1d1d1f; font-weight: 500; margin: 15px 0;"></p>
      <div id="warnBox"></div>

      <div class="advice-grid">
        <div class="advice-card">
          <h3>🎯 重點推分策略</h3>
          <div id="valueAdvice" class="strategy-text"></div>
        </div>
        <div class="advice-card">
          <h3>📚 溫習方向建議</h3>
          <ul id="studyTips" style="margin:0; padding-left:20px; font-size:14px; line-height:1.7;"></ul>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
document.getElementById("calcBtn").addEventListener("click", function() {
  const v = (id) => parseFloat(document.getElementById(id).value) || 0;
  
  // 1. 分數加權計算
  const p1a = v("p1A"), p1b = v("p1B"), p1ae = v("p1AE"), p1be = v("p1BE");
  const p2Raw = [v("p2_1"), v("p2_2"), v("p2_3")].sort((a,b)=>b-a);
  const p2Best = p2Raw[0] + p2Raw[1];

  const p1ap = (p1a/20)*15.5, p1bp = (p1b/20)*15.5;
  const p1aep = (p1ae/25)*19.5, p1bep = (p1be/25)*19.5;
  const p2p = (p2Best/50)*30;
  const total = Math.round((p1ap + p1bp + p1aep + p1bep + p2p) * 10) / 10;

  // 2. 等級評語補全 (Taglines)
  let level = "U", tagline = "";
  if (total >= 82) { level = "5**"; tagline = "整體表現已屬頂尖，卷一盡量維持高命中率，卷二可在觀點深度再作提升。"; }
  else if (total >= 74) { level = "5*"; tagline = "屬高分段，如能收窄粗心失分，加強卷二論述層次感，有機會推上 5**。"; }
  else if (total >= 70) { level = "5"; tagline = "中上水平，建議把卷一當成必須穩守的基礎分，再用卷二拉開差距。"; }
  else if (total >= 60) { level = "4"; tagline = "穩定合格，確保卷一選答題不白白失分，再逐步挑戰卷二較深的題型。"; }
  else if (total >= 50) { level = "3"; tagline = "已有根基，如能再鞏固史實結構，成績有望再上一級。"; }
  else { level = "2/U"; tagline = "目前需要重建大事因果關係，配合簡單資料題技巧，慢慢累積分數。"; }

  document.getElementById("resLvl").innerText = level;
  document.getElementById("resPerc").innerText = total + "%";
  document.getElementById("tagline").innerText = tagline;
  document.getElementById("result").style.display = "block";

  // 3. 補全【重點推分策略】
  const parts = [
    { name: "卷一甲必答", raw: p1a, max: 20, weight: 15.5 },
    { name: "卷一乙必答", raw: p1b, max: 20, weight: 15.5 },
    { name: "卷一甲選答", raw: p1ae, max: 25, weight: 19.5 },
    { name: "卷一乙選答", raw: p1be, max: 25, weight: 19.5 },
    { name: "卷二歷史專題", raw: p2Best, max: 50, weight: 30.0 }
  ];

  const sortedParts = parts.map(p => ({
    name: p.name,
    valPerMark: p.weight / p.max,
    rem: p.max - p.raw,
    potential: (p.max - p.raw) * (p.weight / p.max)
  })).sort((a,b) => b.potential - a.potential);

  const best = sortedParts[0], second = sortedParts[1];
  const aGain = ((20-p1a)*0.775) + ((25-p1ae)*0.78);
  const bGain = ((20-p1b)*0.775) + ((25-p1be)*0.78);
  
  let betterAB = "";
  if (aGain > bGain) betterAB = "從歷代發展整體來看，「甲部」的可提升空間稍大，可優先整理這部分的線索。";
  else if (bGain > aGain) betterAB = "從歷代發展整體來看，「乙部」的可提升空間較多，可先鞏固近現代中國史。";
  else betterAB = "甲部與乙部的提升空間相若，可靈活決定處理順序。";

  let valHtml = "<p>綜合比重與尚可追回的分數後：</p>";
  valHtml += "<p>短期內較適合作為重點推分的是：<strong>" + best.name + "</strong><br>";
  valHtml += "· 每增 1 分 ≈ 全科 <strong>" + best.valPerMark.toFixed(2) + "%</strong><br>";
  valHtml += "· 理論上尚餘 <strong>" + best.rem.toFixed(1) + " 分</strong> 可爭取</p>";
  valHtml += "<hr><p>" + betterAB + "</p>";
  valHtml += "<p style='font-size:12px; color:#86868b;'>卷一是穩定的基礎，卷二則是衝擊 5** 的關鍵分析所在。</p>";
  document.getElementById("valueAdvice").innerHTML = valHtml;

  // 4. 補全【溫習建議】文字
  const tips = document.getElementById("studyTips");
  tips.innerHTML = "";
  const add = (t) => { let li = document.createElement("li"); li.style.marginBottom="10px"; li.innerText = t; tips.appendChild(li); };
  
  add("整體來說，中史卷考三方面：資料價值與限制、分析比較能力、史實熟悉程度。");
  if (total < 55) {
    add("先從「畫大地圖」開始：為甲部和乙部分別整理簡單時間線。");
    add("卷一資料題練習「先捉重點句，再用自己話解釋」。");
    add("開始接觸 Marking Scheme，用螢光筆標出常見關鍵字眼。");
  } else {
    add("熟習五類常見題型：表態、因果、比較、評論及主因題。");
    add("做長題前先打橫寫出段落大綱，確保架構清楚才填入史實。");
    add("檢查卷二時間運用：以每題約 45 分鐘作上限，避免過度糾纏個別史實。");
  }

  // 郭Sir 聯絡提醒
  if (total < 50) {
    document.getElementById("warnBox").innerHTML = "<div style='color:#d70015; font-weight:700; background:#fff2f2; padding:15px; border-radius:12px; margin:10px 0;'>⚠️ 距離目標尚有距離。建議聯絡郭Sir (97701850) 重新制定搶分進度。</div>";
  } else { document.getElementById("warnBox").innerHTML = ""; }

  // 滾動到結果
  window.scrollTo({ top: document.getElementById("result").offsetTop, behavior: 'smooth' });
});
</script>
</body>
</html>
"""

components.html(html_code, height=1400, scrolling=True)
