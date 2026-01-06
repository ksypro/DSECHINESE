import streamlit as st
import streamlit.components.v1 as components

# 設定頁面背景（必須在 Python 層處理一部分，HTML 層處理一部分）
st.set_page_config(page_title="DSE 中史模擬器", layout="wide")

# 這裡的 HTML 包含了完整的 CSS 樣式表，對標你左圖的 UI 設計
html_code = """
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    /* 1. 全局背景與字體 (對標左圖) */
    body {
      background-color: #f0f2f5;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      margin: 0;
      padding: 40px 20px;
      display: flex;
      justify-content: center;
    }

    .main-container {
      max-width: 1000px;
      width: 100%;
    }

    /* 2. 大卡片樣式 */
    .card {
      background: #ffffff;
      border-radius: 24px;
      padding: 40px;
      box-shadow: 0 4px 24px rgba(0, 0, 0, 0.06);
    }

    /* 3. 標題與標籤 */
    h1 { font-size: 32px; font-weight: 800; margin: 0 0 8px 0; color: #1d1d1f; }
    .header-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
    .tag { background: #e8f2ff; color: #0066cc; padding: 4px 12px; border-radius: 20px; font-size: 13px; font-weight: 600; }
    .subtitle { color: #6e6e73; font-size: 15px; line-height: 1.5; margin-bottom: 30px; }

    /* 4. 分數輸入框佈局 (Grid) */
    .section-title { font-size: 13px; font-weight: 700; color: #86868b; text-transform: uppercase; margin: 25px 0 10px 5px; letter-spacing: 0.5px; }
    .inputs-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }

    .input-box {
      border: 1px solid #d2d2d7;
      border-radius: 16px;
      padding: 18px;
      position: relative;
      transition: all 0.2s;
    }
    .input-box:focus-within { border-color: #0066cc; box-shadow: 0 0 0 4px rgba(0, 102, 204, 0.1); }
    
    .input-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
    .input-header label { font-size: 15px; font-weight: 700; color: #1d1d1f; }
    .input-header .weight-tag { font-size: 12px; color: #0066cc; background: #f0f7ff; padding: 2px 8px; border-radius: 4px; }
    
    .real-input {
      width: 100%;
      border: none;
      font-size: 24px;
      font-weight: 500;
      color: #1d1d1f;
      outline: none;
      background: transparent;
      padding: 5px 0;
    }
    .range-hint { position: absolute; right: 18px; bottom: 18px; color: #86868b; font-size: 18px; }
    .desc { font-size: 12px; color: #86868b; margin-top: 8px; line-height: 1.4; }

    /* 5. 按鈕 (漸層藍色) */
    .calc-btn {
      width: 100%;
      background: linear-gradient(135deg, #5e5ce6 0%, #4644d1 100%);
      color: white;
      border: none;
      border-radius: 20px;
      padding: 20px;
      font-size: 18px;
      font-weight: 700;
      cursor: pointer;
      margin-top: 30px;
      transition: transform 0.2s, box-shadow 0.2s;
    }
    .calc-btn:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(94, 92, 230, 0.3); }

    /* 6. 結果顯示區域 */
    .result-section { display: none; margin-top: 30px; border-top: 1px solid #e5e5e5; padding-top: 30px; }
    .level-card { display: flex; align-items: baseline; gap: 15px; margin-bottom: 20px; }
    .level-big { font-size: 56px; font-weight: 800; color: #5e5ce6; }
    .percent-big { font-size: 28px; font-weight: 600; }
    .advice-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin-top: 20px; }
    .advice-item { background: #fbfbfd; border-radius: 16px; padding: 20px; border: 1px solid #d2d2d7; }
    
    /* 手機適應 */
    @media (max-width: 600px) { .inputs-grid, .advice-grid { grid-template-columns: 1fr; } }
  </style>
</head>
<body>
<div class="main-container">
  <div class="card">
    <div class="header-top">
      <h1>DSE 中國歷史 · 成績模擬與溫習規劃</h1>
      <div class="tag">● For S6 Students</div>
    </div>
    <p class="subtitle">輸入你在各部分的預計分數。系統將根據試卷比重計算全科百分比與等級，並給予下一步的溫習重心建議。</p>

    <div class="section-title">PAPER 1 · 必答題 (全科 31%)</div>
    <div class="inputs-grid">
      <div class="input-box">
        <div class="input-header"><label>甲部 必答題</label><span class="weight-tag">20 分 ≈ 全科 15.5%</span></div>
        <input type="number" id="p1AComp" class="real-input" placeholder="0">
        <span class="range-hint">0 - 20</span>
        <div class="desc">範圍：夏、商、周至清（鴉片戰爭前夕）。</div>
      </div>
      <div class="input-box">
        <div class="input-header"><label>乙部 必答題</label><span class="weight-tag">20 分 ≈ 全科 15.5%</span></div>
        <input type="number" id="p1BComp" class="real-input" placeholder="0">
        <span class="range-hint">0 - 20</span>
        <div class="desc">範圍：鴉片戰爭至二十世紀末。</div>
      </div>
    </div>

    <div class="section-title">PAPER 1 · 選答題 (全科 39%)</div>
    <div class="inputs-grid">
      <div class="input-box">
        <div class="input-header"><label>甲部 選答題</label><span class="weight-tag">25 分 ≈ 全科 19.5%</span></div>
        <input type="number" id="p1AElect" class="real-input" placeholder="0">
        <span class="range-hint">0 - 25</span>
        <div class="desc">從甲部 3 題中選 1 題作答。</div>
      </div>
      <div class="input-box">
        <div class="input-header"><label>乙部 選答題</label><span class="weight-tag">25 分 ≈ 全科 19.5%</span></div>
        <input type="number" id="p1BElect" class="real-input" placeholder="0">
        <span class="range-hint">0 - 25</span>
        <div class="desc">從乙部 3 題中選 1 題作答。</div>
      </div>
    </div>

    <div class="section-title">PAPER 2 · 歷史專題 (全科 30%)</div>
    <div class="inputs-grid" style="grid-template-columns: repeat(3, 1fr);">
      <div class="input-box">
        <div class="input-header"><label>黃河流域</label><span class="weight-tag">25 分</span></div>
        <input type="number" id="p2Y" class="real-input" placeholder="0">
        <span class="range-hint">0 - 25</span>
      </div>
      <div class="input-box">
        <div class="input-header"><label>長江流域</label><span class="weight-tag">25 分</span></div>
        <input type="number" id="p2Z" class="real-input" placeholder="0">
        <span class="range-hint">0 - 25</span>
      </div>
      <div class="input-box">
        <div class="input-header"><label>珠江流域</label><span class="weight-tag">25 分</span></div>
        <input type="number" id="p2P" class="real-input" placeholder="0">
        <span class="range-hint">0 - 25</span>
      </div>
    </div>
    <p class="desc" style="margin-top:15px;">註：系統將自動選取分數最高之兩題計算卷二總分。</p>

    <button class="calc-btn" id="calcBtn">計算成績與溫習建議</button>

    <div id="result" class="result-section">
        <div class="level-card">
            <div id="levelText" class="level-big"></div>
            <div id="percentText" class="percent-big"></div>
        </div>
        <p id="taglineText" style="font-size:18px; margin-bottom:20px;"></p>
        <div id="warningText"></div>
        
        <div class="advice-grid">
            <div class="advice-item">
                <h3 style="margin-top:0">🎯 重點推分策略</h3>
                <div id="valueAdvice" style="font-size:14px; line-height:1.6;"></div>
            </div>
            <div class="advice-item">
                <h3 style="margin-top:0">📚 具體溫習方向</h3>
                <ul id="studyTips" style="margin:0; padding-left:20px; font-size:14px; line-height:1.6;"></ul>
            </div>
        </div>
    </div>
  </div>
</div>

<script>
  // 這裡完整保留了你剛才要求的所有 Tagline、加權計算、以及甲乙部潛力分析邏輯
  document.getElementById("calcBtn").addEventListener("click", function() {
    const v = (id) => parseFloat(document.getElementById(id).value) || 0;
    
    // 計算邏輯
    const p1A = v("p1AComp"), p1B = v("p1BComp"), p1AE = v("p1AElect"), p1BE = v("p1BElect");
    const p2Raw = [v("p2Y"), v("p2Z"), v("p2P")].sort((a,b)=>b-a);
    const p2Best = p2Raw[0] + p2Raw[1];

    const p1AP = (p1A/20)*15.5, p1BP = (p1B/20)*15.5;
    const p1AEP = (p1AE/25)*19.5, p1BEP = (p1BE/25)*19.5;
    const p2P = (p2Best/50)*30;
    const total = Math.round((p1AP + p1BP + p1AEP + p1BEP + p2P) * 10) / 10;

    // 等級判定
    let level = "U", tagline = "";
    const cutoffs = [
        { lvl: "5**", s: 82, t: "整體表現已屬頂尖，卷一盡量維持高命中率，卷二則可在觀點深度及史學視角再作提升。" },
        { lvl: "5*", s: 74, t: "屬高分段，如能進一步收窄粗心失分，並加強卷二論述的層次感，有機會推上 5**。" },
        { lvl: "5", s: 70, t: "中上水平，建議把卷一當成必須穩守的基礎分，再用卷二拉開與其他考生的差距。" },
        { lvl: "4", s: 60, t: "已穩定合格，可先確保卷一必答與較熟單元的選答不白白失分，再逐步挑戰卷二較深的題型。" },
        { lvl: "3", s: 50, t: "已有一定根基，如能再鞏固史實與常見題型，並整理好答題結構，成績有望再上一級。" },
        { lvl: "2", s: 30, t: "目前需要打好基本盤，重建各時期大事及因果關係，再配合簡單資料題技巧，慢慢累積分數。" },
        { lvl: "1", s: 1, t: "關鍵是建立整體歷史故事線：搞清次序，再循序漸進學習如何回應題目。" }
    ];

    for (const c of cutoffs) { if (total >= c.s) { level = c.lvl; tagline = c.t; break; } }
    if (total < 1) { level = "U"; tagline = "建議由最基本的時間線重整，逐步接觸簡單論述題。"; }

    // 顯示結果
    document.getElementById("result").style.display = "block";
    document.getElementById("levelText").innerText = level;
    document.getElementById("percentText").innerText = total + "%";
    document.getElementById("taglineText").innerText = tagline;

    // 郭Sir 提醒
    const warn = document.getElementById("warningText");
    if (["3","2","1","U"].includes(level)) {
      warn.innerHTML = "<div style='color:#d70015; font-weight:700; background:#fff2f2; padding:15px; border-radius:12px; margin-bottom:20px;'>⚠️ 模擬等級為 " + level + "。請聯絡郭Sir（97701850）重新規劃溫習進度！</div>";
    } else { warn.innerHTML = ""; }

    // 策略分析 (Value Advice)
    const A_gain = ((20-p1A)*0.775) + ((25-p1AE)*0.78);
    const B_gain = ((20-p1B)*0.775) + ((25-p1BE)*0.78);
    let betterAB = A_gain > B_gain ? "「甲部」提升空間較大。" : "「乙部」提升空間較多。";
    
    document.getElementById("valueAdvice").innerHTML = 
        "<p>綜合計算後，短期內推分重點：<br><strong>" + (A_gain > B_gain ? "卷一 甲部" : "卷一 乙部") + "</strong></p>" +
        "<hr style='border:0; border-top:1px solid #ddd;'>" +
        "<p>" + betterAB + "</p><p style='font-size:12px; color:#86868b;'>卷一是穩守基礎，卷二則是衝擊 5** 的關鍵。</p>";

    // 建議清單
    const tips = document.getElementById("studyTips");
    tips.innerHTML = "";
    const addTip = (txt) => { let li = document.createElement("li"); li.innerText = txt; tips.appendChild(li); };
    
    if (total < 50) {
        addTip("建立時間線，避免掉入細節。");
        addTip("練習「捉重點句，再用自己話解釋」。");
    } else {
        addTip("訓練限時完成論述，一題 45 分鐘內。");
        addTip("整理「範文骨架」，針對評論與比較題型。");
    }
    
    // 自動滾動到結果
    window.scrollTo({ top: document.getElementById("result").offsetTop, behavior: 'smooth' });
  });
</script>
</body>
</html>
"""

# 使用 components.html 渲染，height 設定足夠大以顯示所有內容
components.html(html_code, height=1300, scrolling=True)
