const companies = [
  {
    company_id: "C001",
    company_name: "SampleCompany_001",
    sector: "Manufacturing",
    quarter: "2025Q3",
    operating_margin: 0.118,
    revenue_growth: 0.041,
    debt_ratio: 0.42,
    current_ratio: 1.74,
    volatility: 0.22,
    disclosure_risk: 0.31,
    major_event: false
  },
  {
    company_id: "C003",
    company_name: "SampleCompany_003",
    sector: "Retail",
    quarter: "2025Q3",
    operating_margin: 0.052,
    revenue_growth: -0.037,
    debt_ratio: 0.68,
    current_ratio: 1.08,
    volatility: 0.43,
    disclosure_risk: 0.62,
    major_event: true
  },
  {
    company_id: "C007",
    company_name: "SampleCompany_007",
    sector: "IT",
    quarter: "2025Q3",
    operating_margin: 0.184,
    revenue_growth: 0.092,
    debt_ratio: 0.24,
    current_ratio: 2.42,
    volatility: 0.18,
    disclosure_risk: 0.19,
    major_event: false
  },
  {
    company_id: "C014",
    company_name: "SampleCompany_014",
    sector: "Bio",
    quarter: "2025Q3",
    operating_margin: -0.018,
    revenue_growth: -0.112,
    debt_ratio: 0.74,
    current_ratio: 0.82,
    volatility: 0.58,
    disclosure_risk: 0.78,
    major_event: true
  },
  {
    company_id: "C021",
    company_name: "SampleCompany_021",
    sector: "Finance",
    quarter: "2025Q3",
    operating_margin: 0.096,
    revenue_growth: 0.006,
    debt_ratio: 0.57,
    current_ratio: 1.36,
    volatility: 0.31,
    disclosure_risk: 0.44,
    major_event: false
  }
];

const controls = {
  companySelect: document.getElementById("companySelect"),
  operatingMargin: document.getElementById("operatingMargin"),
  revenueGrowth: document.getElementById("revenueGrowth"),
  debtRatio: document.getElementById("debtRatio"),
  currentRatio: document.getElementById("currentRatio"),
  volatility: document.getElementById("volatility"),
  disclosureRisk: document.getElementById("disclosureRisk"),
  majorEvent: document.getElementById("majorEvent")
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
  gaugeRing: document.getElementById("gaugeRing"),
  overallRisk: document.getElementById("overallRisk"),
  riskNarrative: document.getElementById("riskNarrative"),
  riskExplanation: document.getElementById("riskExplanation"),
  scoreBars: document.getElementById("scoreBars"),
  riskFactors: document.getElementById("riskFactors"),
  positiveFactors: document.getElementById("positiveFactors"),
  decisionJson: document.getElementById("decisionJson"),
  resetButton: document.getElementById("resetButton"),
  downloadButton: document.getElementById("downloadButton"),
  copyJsonButton: document.getElementById("copyJsonButton")
};

function clamp(value, min = 0, max = 1) {
  return Math.min(max, Math.max(min, value));
}

function sigmoid(x) {
  return 1 / (1 + Math.exp(-x));
}

function pct(value) {
  return `${Math.round(value * 100)}%`;
}

function signedPct(value) {
  const sign = value > 0 ? "+" : "";
  return `${sign}${(value * 100).toFixed(1)}%`;
}

function getSelectedCompany() {
  return companies.find((company) => company.company_id === controls.companySelect.value) || companies[0];
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

function score(input) {
  const weakMargin = clamp((0.12 - input.operating_margin) / 0.20);
  const negativeGrowth = clamp((-input.revenue_growth + 0.04) / 0.24);
  const leveragePressure = clamp((input.debt_ratio - 0.35) / 0.55);
  const liquidityPressure = clamp((1.55 - input.current_ratio) / 1.25);
  const marketPressure = clamp((input.volatility - 0.18) / 0.45);
  const disclosurePressure = input.disclosure_risk;
  const eventBoost = input.major_event ? 0.12 : 0;

  const marginDeteriorationRisk = clamp(sigmoid(-1.05 + 1.8 * weakMargin + 1.45 * negativeGrowth + 0.9 * disclosurePressure + eventBoost));
  const marketDrawdownProxyRisk = clamp(sigmoid(-1.00 + 1.75 * marketPressure + 0.95 * leveragePressure + 0.75 * negativeGrowth + 0.55 * disclosurePressure + eventBoost));
  const liquidityStressRisk = clamp(sigmoid(-1.15 + 1.95 * liquidityPressure + 1.30 * leveragePressure + 0.75 * weakMargin + 0.45 * disclosurePressure));
  const averageRisk = clamp((marginDeteriorationRisk + marketDrawdownProxyRisk + liquidityStressRisk) / 3);
  const financialHealthScore = clamp(1 - averageRisk + 0.06 * clamp(input.operating_margin / 0.22) + 0.04 * clamp((input.current_ratio - 1.0) / 2.0));

  return {
    margin_deterioration_risk: marginDeteriorationRisk,
    market_drawdown_proxy_risk: marketDrawdownProxyRisk,
    liquidity_stress_risk: liquidityStressRisk,
    average_risk: averageRisk,
    financial_health_score: financialHealthScore
  };
}

function riskLevel(averageRisk) {
  if (averageRisk >= 0.67) return "high";
  if (averageRisk >= 0.38) return "medium";
  return "low";
}

function riskFactors(input) {
  const factors = [];
  if (input.operating_margin < 0.05) factors.push("Operating margin is weak or negative");
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

function buildPacket(input, scores) {
  const level = riskLevel(scores.average_risk);
  return {
    request_id: `static-demo-${input.company_id}-${Date.now()}`,
    company_id: input.company_id,
    company_name: input.company_name,
    sector: input.sector,
    quarter: input.quarter,
    risk_level: level,
    scores: Object.fromEntries(Object.entries(scores).map(([key, value]) => [key, Number(value.toFixed(4))])),
    top_risk_factors: riskFactors(input),
    positive_factors: positiveFactors(input),
    feature_snapshot: {
      operating_margin: Number(input.operating_margin.toFixed(4)),
      revenue_growth_qoq: Number(input.revenue_growth.toFixed(4)),
      debt_ratio: Number(input.debt_ratio.toFixed(4)),
      current_ratio: Number(input.current_ratio.toFixed(4)),
      volatility_3m: Number(input.volatility.toFixed(4)),
      disclosure_risk_score: Number(input.disclosure_risk.toFixed(4)),
      major_event_flag: input.major_event ? 1 : 0
    },
    demo_scope: "Static GitHub Pages simulator using synthetic examples and explainable heuristic scoring. Not investment advice."
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
  outputs.companyMeta.textContent = `${input.sector} · ${input.quarter} · synthetic sample`;

  const level = riskLevel(scores.average_risk);
  outputs.riskBadge.textContent = level;
  outputs.riskBadge.className = `risk-badge ${level}`;
  outputs.overallRisk.textContent = pct(scores.average_risk);
  outputs.gaugeRing.style.background = `conic-gradient(${level === "high" ? "var(--danger)" : level === "medium" ? "var(--warn)" : "var(--accent)"} ${scores.average_risk * 360}deg, rgba(255,255,255,0.08) 0deg)`;

  const narrativeMap = {
    low: "Low synthetic risk profile",
    medium: "Medium synthetic risk profile",
    high: "High synthetic risk profile"
  };
  outputs.riskNarrative.textContent = narrativeMap[level];
  outputs.riskExplanation.textContent = "This browser result is a product-style preview. The repository backend performs CSV validation, feature generation, model scoring, and artifact creation.";

  const rows = [
    ["Margin deterioration", scores.margin_deterioration_risk],
    ["Market drawdown proxy", scores.market_drawdown_proxy_risk],
    ["Liquidity stress", scores.liquidity_stress_risk],
    ["Financial health", scores.financial_health_score]
  ];
  outputs.scoreBars.innerHTML = rows.map(([label, value]) => `
    <div class="bar-row">
      <div class="bar-label"><span>${label}</span><strong>${pct(value)}</strong></div>
      <div class="bar-track"><div class="bar-fill" style="width:${value * 100}%"></div></div>
    </div>
  `).join("");

  outputs.riskFactors.innerHTML = packet.top_risk_factors.map((item) => `<li>${item}</li>`).join("");
  outputs.positiveFactors.innerHTML = packet.positive_factors.map((item) => `<li>${item}</li>`).join("");
  outputs.decisionJson.textContent = JSON.stringify(packet, null, 2);
}

function render() {
  const input = currentInput();
  const scores = score(input);
  const packet = buildPacket(input, scores);
  updateOutputs(input, scores, packet);
  return packet;
}

function loadCompany(company) {
  controls.operatingMargin.value = company.operating_margin;
  controls.revenueGrowth.value = company.revenue_growth;
  controls.debtRatio.value = company.debt_ratio;
  controls.currentRatio.value = company.current_ratio;
  controls.volatility.value = company.volatility;
  controls.disclosureRisk.value = company.disclosure_risk;
  controls.majorEvent.checked = company.major_event;
  render();
}

function downloadJson() {
  const packet = render();
  const blob = new Blob([JSON.stringify(packet, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `${packet.company_id}_decision_packet_static_demo.json`;
  link.click();
  URL.revokeObjectURL(url);
}

function copyJson() {
  navigator.clipboard?.writeText(outputs.decisionJson.textContent);
  outputs.copyJsonButton.textContent = "복사 완료";
  setTimeout(() => { outputs.copyJsonButton.textContent = "JSON 복사"; }, 1200);
}

function init() {
  controls.companySelect.innerHTML = companies.map((company) => `<option value="${company.company_id}">${company.company_id} · ${company.company_name} · ${company.sector}</option>`).join("");
  controls.companySelect.value = "C003";
  loadCompany(getSelectedCompany());

  controls.companySelect.addEventListener("change", () => loadCompany(getSelectedCompany()));
  Object.values(controls).forEach((control) => {
    if (control && control.id !== "companySelect") control.addEventListener("input", render);
  });
  outputs.resetButton.addEventListener("click", () => loadCompany(getSelectedCompany()));
  outputs.downloadButton.addEventListener("click", downloadJson);
  outputs.copyJsonButton.addEventListener("click", copyJson);
}

init();
