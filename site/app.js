const BASE_COMPANIES = [
  { company_id: "C001", company_name: "Alpha Materials", sector: "Manufacturing", quarter: "2025Q3", operating_margin: 0.118, revenue_growth: 0.041, debt_ratio: 0.42, current_ratio: 1.74, volatility: 0.22, disclosure_risk: 0.31, major_event: false },
  { company_id: "C003", company_name: "Bridge Retail", sector: "Retail", quarter: "2025Q3", operating_margin: 0.052, revenue_growth: -0.037, debt_ratio: 0.68, current_ratio: 1.08, volatility: 0.43, disclosure_risk: 0.62, major_event: true },
  { company_id: "C007", company_name: "Cloud Nine Systems", sector: "IT", quarter: "2025Q3", operating_margin: 0.183, revenue_growth: 0.086, debt_ratio: 0.28, current_ratio: 2.36, volatility: 0.27, disclosure_risk: 0.22, major_event: false },
  { company_id: "C011", company_name: "Delta Bio", sector: "Healthcare", quarter: "2025Q3", operating_margin: -0.024, revenue_growth: -0.091, debt_ratio: 0.54, current_ratio: 1.21, volatility: 0.58, disclosure_risk: 0.49, major_event: false },
  { company_id: "C015", company_name: "Evergreen Energy", sector: "Energy", quarter: "2025Q3", operating_margin: 0.071, revenue_growth: 0.012, debt_ratio: 0.76, current_ratio: 0.92, volatility: 0.51, disclosure_risk: 0.73, major_event: true },
  { company_id: "C020", company_name: "FinCore Holdings", sector: "Financials", quarter: "2025Q3", operating_margin: 0.137, revenue_growth: 0.018, debt_ratio: 0.58, current_ratio: 1.55, volatility: 0.34, disclosure_risk: 0.38, major_event: false }
];

const CSV_EXAMPLE = `company_id,company_name,sector,quarter,operating_margin,revenue_growth,debt_ratio,current_ratio,volatility,disclosure_risk,major_event
U001,Demo Auto,Manufacturing,2025Q3,0.092,-0.018,0.61,1.18,0.39,0.46,false
U002,Demo Cloud,IT,2025Q3,0.205,0.112,0.21,2.41,0.26,0.18,false
U003,Demo Retail,Retail,2025Q3,0.028,-0.082,0.79,0.86,0.55,0.71,true`;

const controls = {
  companySelect: document.getElementById("companySelect"),
  operatingMargin: document.getElementById("operatingMargin"),
  revenueGrowth: document.getElementById("revenueGrowth"),
  debtRatio: document.getElementById("debtRatio"),
  currentRatio: document.getElementById("currentRatio"),
  volatility: document.getElementById("volatility"),
  disclosureRisk: document.getElementById("disclosureRisk"),
  majorEvent: document.getElementById("majorEvent"),
  resetButton: document.getElementById("resetButton"),
  randomizeButton: document.getElementById("randomizeButton"),
  downloadButton: document.getElementById("downloadButton"),
  scenarioButtons: document.getElementById("scenarioButtons"),
  runBatchButton: document.getElementById("runBatchButton"),
  downloadBatchCsvButton: document.getElementById("downloadBatchCsvButton"),
  batchCompanyChecks: document.getElementById("batchCompanyChecks"),
  csvInput: document.getElementById("csvInput"),
  csvFileInput: document.getElementById("csvFileInput"),
  loadCsvExampleButton: document.getElementById("loadCsvExampleButton"),
  scoreCsvButton: document.getElementById("scoreCsvButton"),
  downloadCsvResultButton: document.getElementById("downloadCsvResultButton")
};

const outputs = {
  operatingMarginOut: document.getElementById("operatingMarginOut"),
  revenueGrowthOut: document.getElementById("revenueGrowthOut"),
  debtRatioOut: document.getElementById("debtRatioOut"),
  currentRatioOut: document.getElementById("currentRatioOut"),
  volatilityOut: document.getElementById("volatilityOut"),
  disclosureRiskOut: document.getElementById("disclosureRiskOut"),
  companyTitle: document.getElementById("companyTitle"),
  companyMeta: document.getElementById("companyMeta"),
  riskBadge: document.getElementById("riskBadge"),
  overallRisk: document.getElementById("overallRisk"),
  heroRiskPreview: document.getElementById("heroRiskPreview"),
  gaugeRing: document.getElementById("gaugeRing"),
  riskNarrative: document.getElementById("riskNarrative"),
  riskExplanation: document.getElementById("riskExplanation"),
  scoreBars: document.getElementById("scoreBars"),
  riskFactors: document.getElementById("riskFactors"),
  positiveFactors: document.getElementById("positiveFactors"),
  contributionList: document.getElementById("contributionList"),
  decisionJson: document.getElementById("decisionJson"),
  copyJsonButton: document.getElementById("copyJsonButton"),
  copyCurlButton: document.getElementById("copyCurlButton"),
  batchTableBody: document.querySelector("#batchTable tbody"),
  csvResultTableBody: document.querySelector("#csvResultTable tbody"),
  csvStatus: document.getElementById("csvStatus"),
  apiRequestCode: document.getElementById("apiRequestCode"),
  apiResponseCode: document.getElementById("apiResponseCode"),
  toast: document.getElementById("toast")
};

let currentPacket = null;
let currentBatchRows = [];
let currentCsvRows = [];
let customCompanies = [];

function clamp(value, min = 0, max = 1) {
  return Math.min(max, Math.max(min, Number.isFinite(value) ? value : 0));
}

function pct(value) {
  return `${Math.round(clamp(value) * 100)}%`;
}

function signedPct(value) {
  const num = Number(value) * 100;
  return `${num >= 0 ? "+" : ""}${num.toFixed(1)}%`;
}

function round(value, digits = 4) {
  return Number(Number(value || 0).toFixed(digits));
}

function normalize(value, low, high) {
  return clamp((value - low) / (high - low));
}

function inverseNormalize(value, low, high) {
  return clamp((high - value) / (high - low));
}

function allCompanies() {
  return [...BASE_COMPANIES, ...customCompanies];
}

function getSelectedCompany() {
  const companyId = controls.companySelect.value || BASE_COMPANIES[0].company_id;
  return allCompanies().find((company) => company.company_id === companyId) || BASE_COMPANIES[0];
}

function setActiveScenario(name) {
  controls.scenarioButtons.querySelectorAll(".chip").forEach((button) => {
    button.classList.toggle("active", button.dataset.scenario === name);
  });
}

function applyCompany(company, scenario = "baseline") {
  const input = { ...company };
  if (scenario === "growth") {
    input.operating_margin = clamp(input.operating_margin + 0.045, -0.10, 0.30);
    input.revenue_growth = clamp(input.revenue_growth + 0.07, -0.25, 0.28);
    input.debt_ratio = clamp(input.debt_ratio - 0.08, 0.05, 0.96);
    input.current_ratio = clamp(input.current_ratio + 0.35, 0.40, 3.80);
    input.volatility = clamp(input.volatility - 0.07, 0.04, 0.85);
    input.disclosure_risk = clamp(input.disclosure_risk - 0.16, 0, 1);
    input.major_event = false;
  }
  if (scenario === "marginShock") {
    input.operating_margin = clamp(input.operating_margin - 0.085, -0.10, 0.30);
    input.revenue_growth = clamp(input.revenue_growth - 0.055, -0.25, 0.28);
    input.volatility = clamp(input.volatility + 0.06, 0.04, 0.85);
  }
  if (scenario === "liquidityCrunch") {
    input.debt_ratio = clamp(input.debt_ratio + 0.18, 0.05, 0.96);
    input.current_ratio = clamp(input.current_ratio - 0.58, 0.40, 3.80);
    input.disclosure_risk = clamp(input.disclosure_risk + 0.12, 0, 1);
  }
  if (scenario === "marketStress") {
    input.volatility = clamp(input.volatility + 0.23, 0.04, 0.85);
    input.revenue_growth = clamp(input.revenue_growth - 0.035, -0.25, 0.28);
    input.disclosure_risk = clamp(input.disclosure_risk + 0.08, 0, 1);
  }
  if (scenario === "eventShock") {
    input.major_event = true;
    input.disclosure_risk = clamp(input.disclosure_risk + 0.30, 0, 1);
    input.volatility = clamp(input.volatility + 0.11, 0.04, 0.85);
  }

  controls.operatingMargin.value = input.operating_margin;
  controls.revenueGrowth.value = input.revenue_growth;
  controls.debtRatio.value = input.debt_ratio;
  controls.currentRatio.value = input.current_ratio;
  controls.volatility.value = input.volatility;
  controls.disclosureRisk.value = input.disclosure_risk;
  controls.majorEvent.checked = Boolean(input.major_event);
  render();
}

function currentInput() {
  const base = getSelectedCompany();
  return {
    ...base,
    operating_margin: Number(controls.operatingMargin.value),
    revenue_growth: Number(controls.revenueGrowth.value),
    debt_ratio: Number(controls.debtRatio.value),
    current_ratio: Number(controls.currentRatio.value),
    volatility: Number(controls.volatility.value),
    disclosure_risk: Number(controls.disclosureRisk.value),
    major_event: controls.majorEvent.checked
  };
}

function computeScores(input) {
  const marginWeakness = inverseNormalize(input.operating_margin, 0.02, 0.16);
  const revenuePressure = inverseNormalize(input.revenue_growth, -0.08, 0.08);
  const debtPressure = normalize(input.debt_ratio, 0.35, 0.82);
  const liquidityPressure = inverseNormalize(input.current_ratio, 0.85, 1.9);
  const marketPressure = normalize(input.volatility, 0.16, 0.62);
  const disclosurePressure = clamp(input.disclosure_risk);
  const eventPressure = input.major_event ? 1 : 0;

  const marginDeteriorationRisk = clamp(
    0.48 * marginWeakness +
    0.28 * revenuePressure +
    0.14 * disclosurePressure +
    0.10 * eventPressure
  );
  const marketDrawdownProxyRisk = clamp(
    0.50 * marketPressure +
    0.17 * debtPressure +
    0.20 * disclosurePressure +
    0.13 * eventPressure
  );
  const liquidityStressRisk = clamp(
    0.45 * liquidityPressure +
    0.30 * debtPressure +
    0.15 * revenuePressure +
    0.10 * eventPressure
  );
  const averageRisk = clamp(
    0.38 * marginDeteriorationRisk +
    0.32 * marketDrawdownProxyRisk +
    0.30 * liquidityStressRisk
  );
  const financialHealthScore = clamp(1 - averageRisk + 0.06 * normalize(input.operating_margin, 0.08, 0.20) + 0.04 * normalize(input.current_ratio, 1.25, 2.4));

  return {
    margin_deterioration_risk: marginDeteriorationRisk,
    market_drawdown_proxy_risk: marketDrawdownProxyRisk,
    liquidity_stress_risk: liquidityStressRisk,
    average_risk: averageRisk,
    financial_health_score: financialHealthScore,
    internals: { marginWeakness, revenuePressure, debtPressure, liquidityPressure, marketPressure, disclosurePressure, eventPressure }
  };
}

function riskLevel(averageRisk) {
  if (averageRisk >= 0.67) return "high";
  if (averageRisk >= 0.38) return "medium";
  return "low";
}

function topFactor(input) {
  return riskFactors(input)[0] || "No dominant red flag";
}

function riskFactors(input) {
  const factors = [];
  if (input.operating_margin < 0.04) factors.push("Operating margin is weak or negative");
  if (input.revenue_growth < -0.03) factors.push("Quarter-over-quarter revenue growth is deteriorating");
  if (input.debt_ratio > 0.65) factors.push("Debt ratio is elevated");
  if (input.current_ratio < 1.15) factors.push("Current ratio suggests liquidity pressure");
  if (input.volatility > 0.40) factors.push("Recent market volatility is high");
  if (input.disclosure_risk > 0.60) factors.push("Disclosure-derived risk signal is elevated");
  if (input.major_event) factors.push("Major event flag requires human review");
  return factors.length ? factors : ["No dominant red flag in the current synthetic profile"];
}

function positiveFactors(input) {
  const factors = [];
  if (input.operating_margin >= 0.12) factors.push("Operating margin is relatively strong");
  if (input.revenue_growth >= 0.04) factors.push("Revenue growth is positive");
  if (input.debt_ratio <= 0.40) factors.push("Debt ratio is conservative");
  if (input.current_ratio >= 1.60) factors.push("Liquidity buffer looks healthy");
  if (input.volatility <= 0.24) factors.push("Recent volatility is contained");
  if (input.disclosure_risk <= 0.30) factors.push("Disclosure risk signal is low");
  return factors.length ? factors : ["Positive signals are limited in the current synthetic profile"];
}

function contributionRows(input, scores) {
  const internals = scores.internals;
  return [
    { label: "Operating margin weakness", value: internals.marginWeakness, note: input.operating_margin < 0.04 ? "risk up" : "stable" },
    { label: "Revenue growth pressure", value: internals.revenuePressure, note: input.revenue_growth < 0 ? "risk up" : "stable" },
    { label: "Debt pressure", value: internals.debtPressure, note: input.debt_ratio > 0.65 ? "risk up" : "contained" },
    { label: "Liquidity pressure", value: internals.liquidityPressure, note: input.current_ratio < 1.15 ? "risk up" : "buffer" },
    { label: "Market volatility", value: internals.marketPressure, note: input.volatility > 0.40 ? "risk up" : "contained" },
    { label: "Disclosure / event signal", value: Math.max(internals.disclosurePressure, internals.eventPressure), note: input.major_event ? "human review" : "monitor" }
  ].sort((a, b) => b.value - a.value);
}

function buildPacket(input, scores) {
  const level = riskLevel(scores.average_risk);
  return {
    request_id: `static-live-lab-${input.company_id}-${Date.now()}`,
    source: "GitHub Pages browser simulator",
    company_id: input.company_id,
    company_name: input.company_name,
    sector: input.sector,
    quarter: input.quarter,
    risk_level: level,
    scores: {
      margin_deterioration_risk: round(scores.margin_deterioration_risk),
      market_drawdown_proxy_risk: round(scores.market_drawdown_proxy_risk),
      liquidity_stress_risk: round(scores.liquidity_stress_risk),
      average_risk: round(scores.average_risk),
      financial_health_score: round(scores.financial_health_score)
    },
    top_risk_factors: riskFactors(input),
    positive_factors: positiveFactors(input),
    feature_snapshot: {
      operating_margin: round(input.operating_margin),
      revenue_growth_qoq: round(input.revenue_growth),
      debt_ratio: round(input.debt_ratio),
      current_ratio: round(input.current_ratio),
      volatility_3m: round(input.volatility),
      disclosure_risk_score: round(input.disclosure_risk),
      major_event_flag: input.major_event ? 1 : 0
    },
    model_explanations: contributionRows(input, scores).slice(0, 4).map((row) => ({
      feature: row.label,
      contribution_preview: round(row.value),
      note: row.note
    })),
    demo_scope: "Static GitHub Pages simulator using synthetic examples and explainable heuristic scoring. The real Python/FastAPI backend is separate. Not investment advice."
  };
}

function updateOutputs(input, scores, packet) {
  outputs.operatingMarginOut.textContent = signedPct(input.operating_margin);
  outputs.revenueGrowthOut.textContent = signedPct(input.revenue_growth);
  outputs.debtRatioOut.textContent = pct(input.debt_ratio);
  outputs.currentRatioOut.textContent = input.current_ratio.toFixed(2);
  outputs.volatilityOut.textContent = pct(input.volatility);
  outputs.disclosureRiskOut.textContent = pct(input.disclosure_risk);

  outputs.companyTitle.textContent = `${input.company_name} (${input.company_id})`;
  outputs.companyMeta.textContent = `${input.sector} · ${input.quarter} · synthetic/browser sample`;

  const level = riskLevel(scores.average_risk);
  outputs.riskBadge.textContent = level;
  outputs.riskBadge.className = `risk-badge ${level}`;
  outputs.overallRisk.textContent = pct(scores.average_risk);
  outputs.heroRiskPreview.textContent = pct(scores.average_risk);

  const color = level === "high" ? "var(--danger)" : level === "medium" ? "var(--warn)" : "var(--accent)";
  outputs.gaugeRing.style.background = `conic-gradient(${color} ${scores.average_risk * 360}deg, rgba(255,255,255,0.08) 0deg)`;

  const narrativeMap = {
    low: "Low synthetic risk profile",
    medium: "Medium synthetic risk profile",
    high: "High synthetic risk profile"
  };
  const explanationMap = {
    low: "현재 입력값은 큰 적색 신호가 적습니다. 실제 백엔드에서는 CSV validation, feature engineering, model scoring, monitoring artifact까지 생성합니다.",
    medium: "일부 지표에서 주의 신호가 있습니다. 리스크 요인과 positive signal을 함께 보며 human review로 연결하는 흐름을 보여줍니다.",
    high: "복수의 리스크 신호가 동시에 올라왔습니다. 포트폴리오상 핵심은 위험 판단 자체보다 packet, explanation, API boundary를 만드는 능력입니다."
  };
  outputs.riskNarrative.textContent = narrativeMap[level];
  outputs.riskExplanation.textContent = explanationMap[level];

  const rows = [
    ["Margin deterioration", scores.margin_deterioration_risk],
    ["Market drawdown proxy", scores.market_drawdown_proxy_risk],
    ["Liquidity stress", scores.liquidity_stress_risk],
    ["Financial health", scores.financial_health_score]
  ];
  outputs.scoreBars.innerHTML = rows.map(([label, value]) => `
    <div class="bar-row">
      <div class="bar-label"><span>${label}</span><strong>${pct(value)}</strong></div>
      <div class="bar-track"><div class="bar-fill" style="width:${clamp(value) * 100}%"></div></div>
    </div>
  `).join("");

  outputs.riskFactors.innerHTML = packet.top_risk_factors.map((item) => `<li>${escapeHtml(item)}</li>`).join("");
  outputs.positiveFactors.innerHTML = packet.positive_factors.map((item) => `<li>${escapeHtml(item)}</li>`).join("");
  outputs.contributionList.innerHTML = contributionRows(input, scores).map((row) => `
    <div class="contribution-row">
      <header><span>${escapeHtml(row.label)}</span><strong>${pct(row.value)} · ${escapeHtml(row.note)}</strong></header>
      <div class="contribution-track"><div class="contribution-fill" style="width:${clamp(row.value) * 100}%"></div></div>
    </div>
  `).join("");
  outputs.decisionJson.textContent = JSON.stringify(packet, null, 2);

  const apiRequest = {
    method: "POST",
    path: "/v1/predictions",
    body: {
      company_id: input.company_id,
      input_dir: "data/input/sample",
      artifact_dir: "artifacts"
    }
  };
  outputs.apiRequestCode.textContent = `# Request preview\n${JSON.stringify(apiRequest, null, 2)}`;
  outputs.apiResponseCode.textContent = `# Response preview\n${JSON.stringify(packet, null, 2)}`;
}

function render() {
  const input = currentInput();
  const scores = computeScores(input);
  currentPacket = buildPacket(input, scores);
  updateOutputs(input, scores, currentPacket);
}

function renderCompanyOptions() {
  controls.companySelect.innerHTML = allCompanies().map((company) => (
    `<option value="${escapeHtml(company.company_id)}">${escapeHtml(company.company_id)} · ${escapeHtml(company.company_name)}</option>`
  )).join("");
}

function renderBatchChecks() {
  controls.batchCompanyChecks.innerHTML = allCompanies().map((company, index) => `
    <label class="check-pill">
      <input type="checkbox" value="${escapeHtml(company.company_id)}" ${index < 6 ? "checked" : ""} />
      ${escapeHtml(company.company_id)} ${escapeHtml(company.company_name)}
    </label>
  `).join("");
}

function scoreCompany(company) {
  const scores = computeScores(company);
  const packet = buildPacket(company, scores);
  return {
    ...company,
    level: packet.risk_level,
    average_risk: scores.average_risk,
    margin: scores.margin_deterioration_risk,
    market: scores.market_drawdown_proxy_risk,
    liquidity: scores.liquidity_stress_risk,
    top_factor: topFactor(company),
    packet
  };
}

function runBatch(companyIds = null) {
  const selectedIds = companyIds || Array.from(controls.batchCompanyChecks.querySelectorAll("input:checked")).map((input) => input.value);
  const rows = allCompanies()
    .filter((company) => selectedIds.includes(company.company_id))
    .map(scoreCompany)
    .sort((a, b) => b.average_risk - a.average_risk);
  currentBatchRows = rows;
  outputs.batchTableBody.innerHTML = rows.map((row, index) => `
    <tr>
      <td>${index + 1}</td>
      <td><strong>${escapeHtml(row.company_id)}</strong><br><span class="muted">${escapeHtml(row.company_name)}</span></td>
      <td>${escapeHtml(row.sector)}</td>
      <td><span class="level-dot ${row.level}">${escapeHtml(row.level)}</span></td>
      <td>${pct(row.average_risk)}</td>
      <td>${pct(row.margin)}</td>
      <td>${pct(row.market)}</td>
      <td>${pct(row.liquidity)}</td>
      <td>${escapeHtml(row.top_factor)}</td>
    </tr>
  `).join("");
  showToast(`${rows.length}개 회사 batch scoring 완료`);
}

function parseCsv(text) {
  const rows = text.trim().split(/\r?\n/).filter(Boolean);
  if (rows.length < 2) return [];
  const headers = rows[0].split(",").map((item) => item.trim());
  return rows.slice(1).map((line, index) => {
    const values = line.split(",").map((item) => item.trim());
    const obj = Object.fromEntries(headers.map((key, i) => [key, values[i] ?? ""]));
    return {
      company_id: obj.company_id || `CSV${index + 1}`,
      company_name: obj.company_name || obj.name || `CSV Company ${index + 1}`,
      sector: obj.sector || "Unknown",
      quarter: obj.quarter || "2025Q3",
      operating_margin: Number(obj.operating_margin || 0),
      revenue_growth: Number(obj.revenue_growth || obj.revenue_growth_qoq || 0),
      debt_ratio: Number(obj.debt_ratio || 0.5),
      current_ratio: Number(obj.current_ratio || 1.3),
      volatility: Number(obj.volatility || obj.volatility_3m || 0.3),
      disclosure_risk: Number(obj.disclosure_risk || obj.disclosure_risk_score || 0.3),
      major_event: String(obj.major_event || obj.major_event_flag || "false").toLowerCase() === "true" || String(obj.major_event_flag) === "1"
    };
  }).filter((row) => row.company_id && Number.isFinite(row.operating_margin));
}

function scoreCsv() {
  const rows = parseCsv(controls.csvInput.value);
  currentCsvRows = rows.map(scoreCompany).sort((a, b) => b.average_risk - a.average_risk);
  outputs.csvResultTableBody.innerHTML = currentCsvRows.map((row) => `
    <tr>
      <td><strong>${escapeHtml(row.company_id)}</strong><br><span class="muted">${escapeHtml(row.company_name)}</span></td>
      <td><span class="level-dot ${row.level}">${escapeHtml(row.level)}</span></td>
      <td>${pct(row.average_risk)}</td>
      <td>${escapeHtml(row.top_factor)}</td>
    </tr>
  `).join("");
  outputs.csvStatus.textContent = currentCsvRows.length
    ? `${currentCsvRows.length}개 row를 브라우저에서 스코어링했습니다. 서버로 전송하지 않습니다.`
    : "CSV를 읽지 못했습니다. header와 숫자 형식을 확인하세요.";
  if (rows.length) {
    customCompanies = mergeCustomCompanies(rows);
    renderCompanyOptions();
    renderBatchChecks();
    showToast("CSV 회사가 샘플 목록에 추가되었습니다");
  }
}

function mergeCustomCompanies(rows) {
  const baseIds = new Set(BASE_COMPANIES.map((company) => company.company_id));
  const unique = new Map(customCompanies.filter((company) => !baseIds.has(company.company_id)).map((company) => [company.company_id, company]));
  rows.forEach((row) => unique.set(row.company_id, row));
  return Array.from(unique.values());
}

function toCsv(rows) {
  const header = ["rank", "company_id", "company_name", "sector", "risk_level", "average_risk", "margin_deterioration", "market_drawdown_proxy", "liquidity_stress", "top_factor"];
  const body = rows.map((row, index) => [
    index + 1,
    row.company_id,
    row.company_name,
    row.sector,
    row.level,
    round(row.average_risk),
    round(row.margin),
    round(row.market),
    round(row.liquidity),
    row.top_factor
  ]);
  return [header, ...body].map((items) => items.map(csvEscape).join(",")).join("\n");
}

function csvEscape(value) {
  const text = String(value ?? "");
  return /[",\n]/.test(text) ? `"${text.replace(/"/g, '""')}"` : text;
}

function downloadText(filename, text, type = "application/json") {
  const blob = new Blob([text], { type });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = filename;
  document.body.appendChild(anchor);
  anchor.click();
  anchor.remove();
  URL.revokeObjectURL(url);
}

async function copyText(text, message) {
  try {
    await navigator.clipboard.writeText(text);
    showToast(message || "복사했습니다");
  } catch (_error) {
    const area = document.createElement("textarea");
    area.value = text;
    document.body.appendChild(area);
    area.select();
    document.execCommand("copy");
    area.remove();
    showToast(message || "복사했습니다");
  }
}

function buildCurl(input) {
  return `curl -X POST http://127.0.0.1:8000/v1/predictions \\\n  -H "Content-Type: application/json" \\\n  -d '{"company_id":"${input.company_id}","input_dir":"data/input/sample","artifact_dir":"artifacts"}'`;
}

function randomCompany() {
  const id = `R${Math.floor(100 + Math.random() * 900)}`;
  return {
    company_id: id,
    company_name: `RandomCo_${id}`,
    sector: ["Manufacturing", "Retail", "IT", "Healthcare", "Energy"][Math.floor(Math.random() * 5)],
    quarter: "2025Q3",
    operating_margin: randomBetween(-0.04, 0.22),
    revenue_growth: randomBetween(-0.13, 0.16),
    debt_ratio: randomBetween(0.20, 0.88),
    current_ratio: randomBetween(0.72, 2.75),
    volatility: randomBetween(0.12, 0.68),
    disclosure_risk: randomBetween(0.08, 0.86),
    major_event: Math.random() > 0.78
  };
}

function randomBetween(min, max) {
  return round(min + Math.random() * (max - min), 3);
}

function showToast(message) {
  outputs.toast.textContent = message;
  outputs.toast.classList.add("show");
  clearTimeout(showToast.timeout);
  showToast.timeout = setTimeout(() => outputs.toast.classList.remove("show"), 1900);
}

function escapeHtml(value) {
  return String(value).replace(/[&<>'"]/g, (char) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    "'": "&#39;",
    '"': "&quot;"
  }[char]));
}

function init() {
  renderCompanyOptions();
  renderBatchChecks();
  controls.companySelect.value = "C003";
  applyCompany(getSelectedCompany());
  controls.csvInput.value = CSV_EXAMPLE;
  runBatch();
  scoreCsv();
  controls.companySelect.value = "C003";
  applyCompany(getSelectedCompany());

  controls.companySelect.addEventListener("change", () => {
    setActiveScenario("baseline");
    applyCompany(getSelectedCompany());
  });
  [controls.operatingMargin, controls.revenueGrowth, controls.debtRatio, controls.currentRatio, controls.volatility, controls.disclosureRisk, controls.majorEvent].forEach((control) => {
    control.addEventListener("input", () => {
      setActiveScenario("custom");
      render();
    });
  });
  controls.scenarioButtons.addEventListener("click", (event) => {
    const button = event.target.closest("button[data-scenario]");
    if (!button) return;
    const scenario = button.dataset.scenario;
    setActiveScenario(scenario);
    applyCompany(getSelectedCompany(), scenario);
    showToast(`${button.textContent.trim()} 적용됨`);
  });
  controls.resetButton.addEventListener("click", () => {
    setActiveScenario("baseline");
    applyCompany(getSelectedCompany());
    showToast("샘플값으로 리셋했습니다");
  });
  controls.randomizeButton.addEventListener("click", () => {
    const company = randomCompany();
    customCompanies = mergeCustomCompanies([company]);
    renderCompanyOptions();
    renderBatchChecks();
    controls.companySelect.value = company.company_id;
    setActiveScenario("baseline");
    applyCompany(company);
    showToast("랜덤 회사가 생성되었습니다");
  });
  controls.downloadButton.addEventListener("click", () => {
    downloadText(`${currentPacket.company_id}_decision_packet.json`, JSON.stringify(currentPacket, null, 2));
  });
  outputs.copyJsonButton.addEventListener("click", () => copyText(JSON.stringify(currentPacket, null, 2), "Decision packet JSON 복사 완료"));
  outputs.copyCurlButton.addEventListener("click", () => copyText(buildCurl(currentInput()), "cURL 예시 복사 완료"));
  controls.runBatchButton.addEventListener("click", () => runBatch());
  controls.downloadBatchCsvButton.addEventListener("click", () => {
    if (!currentBatchRows.length) runBatch();
    downloadText("batch_risk_scores.csv", toCsv(currentBatchRows), "text/csv");
  });
  controls.loadCsvExampleButton.addEventListener("click", () => {
    controls.csvInput.value = CSV_EXAMPLE;
    showToast("예시 CSV를 넣었습니다");
  });
  controls.scoreCsvButton.addEventListener("click", scoreCsv);
  controls.downloadCsvResultButton.addEventListener("click", () => {
    if (!currentCsvRows.length) scoreCsv();
    downloadText("csv_risk_scores.csv", toCsv(currentCsvRows), "text/csv");
  });
  controls.csvFileInput.addEventListener("change", async (event) => {
    const file = event.target.files?.[0];
    if (!file) return;
    controls.csvInput.value = await file.text();
    showToast(`${file.name} 불러옴`);
  });
}

init();
