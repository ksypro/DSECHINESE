import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="DSE 中史模擬器", layout="wide")

# 這裡封裝了你原本所有的計算邏輯與文字
html_code = """
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8">
  <style>
    * { box-sizing: border-box; }
    body { font-family: -apple-system, sans-serif; background: #f5f5f7; padding: 15px; color: #1d1d1f; }
    .container { max-width: 900px; margin: auto; }
    .card { background: white; border-radius: 18px; padding: 25px; box-shadow: 0 8px 30px rgba(0,0,0,0.05); margin-bottom: 20px; }
    h1 { font-size: 26px; font-weight: 800; }
    .subtitle { font-size: 14px; color: #6e6e73; margin-bottom: 20px; }
    .inputs-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; }
    .input-group { background: #fbfbfd; border-radius: 12px; padding: 12px; border: 1px solid #d2d2d7; }
    label { font-size: 13px; font-weight: 600; display: block; margin-bottom: 5px; }
    input { width: 100%; padding: 10px; border-radius: 8px; border: 1px solid #d2d2d7; font-size: 16px; }
    button { width: 100%; padding: 16px; background: #0071e3; color: white; border: none; border-radius: 12px; font-size: 16px; font-weight: 600; cursor: pointer; margin-top: 20px; }
    .result-section { display: none; }
    .level-display { display: flex; align-items: baseline; gap: 10px; }
    .level { font-size: 48px; font-weight: 800; color: #0071e3; }
    .percent { font-size: 24px; color: #1d1d1f; }
    .warning { color: #d70015; font-weight: 700; margin: 15px 0; padding: 10px; border-left: 4px solid #d70015; background: #fff2f2; }
    .small-card { background: #fbfbfd; border-radius: 12px; padding: 15px; border: 1px solid #d2d2d7; margin-top: 15px; }
    h3 { font-size: 15px; margin-top: 0; }
    ul { padding-left: 20px; font-size: 13px; line-height: 1.7; }
    .subtle { font-size: 11px; color: #86868b; margin-top: 5px; }
    hr { border: 0; border-top: 1px solid #d2d2d7; margin: 15px 0; }
  </style>
</head>
<body>
<div class="container">
  <div class="card">
    <h1>DSE 中國歷史 · 成績模擬與溫習規劃</h1>
    <p class="subtitle">輸入預算分數，獲取 郭Sir 專屬分析與 Tagline 評語。</p>
    
    <div class="inputs-grid">
      <div class="input-group"><label>卷一：甲必答 (20)</label><input id="p1AComp" type="number" max="20" value="0"></div>
      <div class="input-group"><label>卷一：乙必答 (20)</label><input id="p1BComp" type="number" max="20" value="0"></div>
      <div class="input-group"><label>卷一：甲選答 (25)</label><input id="p1AElect" type="number" max="25" value="0"></div>
      <div class="input-group"><label>卷一：乙選答 (25)</label><input id="p1BElect" type="number" max="25" value="0"></div>
      <div class="input-group"><label>卷二：黃河 (25)</label><input id="p2Y" type="number" max="25" value="0"></div>
      <div class="input-group"><label>卷二：長江 (25)</label><input id="p2Z" type="number" max="25" value="0"></div>
      <div class="input-group"><label>卷二：珠江 (25)</label><input id="p2P" type="number" max="25" value="0"></div>
    </div>
    <button id="calcBtn">計算模擬結果</button>
  </div>

  <div id="result" class="card result-section">
    <div class="level-display">
      <div id="levelText" class="level"></div>
      <div id="percentText" class="percent"></div>
    </div>
    <p id="taglineText" style="font-weight: 500; color: #3a3a3c; margin: 10px 0;"></p>
    <div id="warningText"></div>

    <div class="small-card">
      <h3>重點推分策略</h3>
      <div id="valueAdvice"></div>
    </div>

    <div class="small-card">
      <h3>具體溫習建議</h3>
      <ul id="studyTips"></ul>
    </div>
  </div>
</div>

<script>
  document.getElementById("calcBtn").addEventListener("click", function() {
    const v = (id) => parseFloat(document.getElementById(id).value) || 0;
    
    // 獲取分數
    const p1A = v("p1AComp"), p1B = v("p1BComp"), p1AE = v("p1AElect"), p1BE = v("p1BElect");
    const p2Raw = [v("p2Y"), v("p2Z"), v("p2P")].sort((a,b)=>b-a);
    const p2Best = p2Raw[0] + p2Raw[1];

    // 計算加權
    const p1AP = (p1A/20)*15.5, p1BP = (p1B/20)*15.5;
    const p1AEP = (p1AE/25)*19.5, p1BEP = (p1BE/25)*19.5;
    const p2P = (p2Best/50)*30;
    const total = Math.round((p1AP + p1BP + p1AEP + p1BEP + p2P) * 10) / 10;

    // 1. 等級評語 (Tagline)
    let level = "U", tagline = "";
    if (total >= 82) { level = "5**"; tagline = "整體表現已屬頂尖，卷一盡量維持高命中率，卷二則可在觀點深度及史學視角再作提升。"; }
    else if (total >= 74) { level = "5*"; tagline = "屬高分段，如能進一步收窄粗心失分，並加強卷二論述的層次感，有機會推上 5**。"; }
    else if (total >= 70) { level = "5"; tagline = "中上水平，建議把卷一當成必須穩守的基礎分，再用卷二拉開與其他考生的差距。"; }
    else if (total >= 60) { level = "4"; tagline = "已穩定合格，可先確保卷一必答與較熟單元的選答不白白失分，再逐步挑戰卷二較深的題型。"; }
    else if (total >= 50) { level = "3"; tagline = "已有一定根基，如能再鞏固史實與常見題型，並整理好答題結構，成績有望再上一級。"; }
    else if (total >= 30) { level = "2"; tagline = "目前需要打好基本盤，重建各時期大事及因果關係，再配合簡單資料題技巧，慢慢累積分數。"; }
    else if (total >= 1) { level = "1"; tagline = "關鍵是建立整體歷史故事線：先搞清每一階段發生什麼事與大概次序，再循序漸進學習如何用資料與史實回應題目。"; }
    else { level = "U"; tagline = "暫時未達第 1 級，建議由最基本的時間線與大事開始重整，再逐步接觸資料題與簡單論述題。"; }

    document.getElementById("levelText").innerText = "等級：" + level;
    document.getElementById("percentText").innerText = total + "%";
    document.getElementById("taglineText").innerText = tagline;
    document.getElementById("result").style.display = "block";

    // 2. 郭Sir 聯絡提醒
    const warn = document.getElementById("warningText");
    if (["3","2","1","U"].includes(level)) {
      warn.className = "warning";
      warn.innerText = "⚠️ 模擬結果顯示你目前大約在「第 " + level + " 級」水平。請立即聯絡郭Sir（97701850），改變始於今日。";
    } else { warn.className = ""; warn.innerText = ""; }

    // 3. 提升空間分析 (BetterAB & ValueAdvice)
    const parts = [
      { name: "卷一甲必答", raw: p1A, max: 20, weight: 15.5 },
      { name: "卷一乙必答", raw: p1B, max: 20, weight: 15.5 },
      { name: "卷一甲選答", raw: p1AE, max: 25, weight: 19.5 },
      { name: "卷一乙選答", raw: p1BE, max: 25, weight: 19.5 }
    ];
    
    const partsWithValue = parts.map(p => ({
      name: p.name,
      percentPerMark: p.weight / p.max,
      remainingMarks: p.max - p.raw,
      potentialGain: (p.max - p.raw) * (p.weight / p.max)
    })).sort((a, b) => b.potentialGain - a.potentialGain);

    const bestPart = partsWithValue[0];
    const secondBestPart = partsWithValue[1];

    // 甲 vs 乙 整體比較
    const A_gain = ( (20-p1A)*(15.5/20) ) + ( (25-p1AE)*(19.5/25) );
    const B_gain = ( (20-p1B)*(15.5/20) ) + ( (25-p1BE)*(19.5/25) );
    let betterAB = "";
    if (A_gain > B_gain) betterAB = "從歷代發展整體來看，「甲部」（夏商周至鴉片戰爭前夕）的可提升空間稍大，可以優先整理這部分的線索及重要政策。";
    else if (B_gain > A_gain) betterAB = "從歷代發展整體來看，「乙部」（鴉片戰爭至二十世紀末）的可提升空間較多，可先鞏固近現代中國史，並配合資料題與論述題練習。";
    else betterAB = "現階段，歷代發展中的甲部與乙部整體提升空間相若，靈活決定先處理哪一邊。";

    let valHtml = "<p>因為各部分的比重與尚可追回的分數不同，綜合計算後：</p>";
    valHtml += "<p>短期內較適合作為重點推分的是：<strong>" + bestPart.name + "</strong><br>";
    valHtml += "· 每增加 1 分，約相當於全科 <strong>" + bestPart.percentPerMark.toFixed(2) + "%</strong><br>";
    valHtml += "· 理論上尚餘約 <strong>" + bestPart.remainingMarks + " 分</strong> 可爭取</p>";
    valHtml += "<p>第二重點可考慮：<strong>" + secondBestPart.name + "</strong>。</p>";
    valHtml += "<hr><p>" + betterAB + "</p>";
    valHtml += "<p class='subtle'>方向：卷一穩守基礎；卷二則是分辨 5、5*、5** 的關鍵。</p>";
    document.getElementById("valueAdvice").innerHTML = valHtml;

    // 4. 具體建議 (補全丟失的建議文字)
    const tips = document.getElementById("studyTips");
    tips.innerHTML = "";
    const addTip = (t) => { let li = document.createElement("li"); li.innerText = t; tips.appendChild(li); };
    
    addTip("【共通提醒】中史卷考三方面：資料價值與限制、分析比較能力、史實熟悉度。");

    if (total < 30) {
      addTip("先從「畫大地圖」開始：為甲部和乙部分別整理簡單時間線及關鍵事件。");
      addTip("卷一資料題練習「先捉重點句，再用自己話解釋」。");
      addTip("接觸 Past Paper Marking Scheme，用螢光筆標出常見字眼。");
    } else if (total < 50) {
      addTip("操卷時用 Marking Scheme 反推溫習方向：點列方式抄下重點句。");
      addTip("回答資料限制時，從作者、時間、種類三個角度入手。");
      addTip("卷一答題設計固定結構：論點 -> 引用 -> 解說 -> 小結。");
    } else if (total < 70) {
      addTip("訓練限時完成：嘗試在 45 分鐘內寫出結構完整的答案。");
      addTip("熟習五類常見題型：表態、因果、比較、評論及主因題。");
      addTip("卷二嘗試在答案中清楚分段，包含立場句、史實及解說。");
    } else {
      addTip("檢視失分題：區分是史實記錯、理解方向有誤還是論證不緊密。");
      addTip("刻意多練評論題與主因題：比較不同原因的份量。");
      addTip("替每個專題整理「範文骨架」，有助考試時快速起稿。");
    }
  });
</script>
</body>
</html>
"""

components.html(html_code, height=1300, scrolling=True)
