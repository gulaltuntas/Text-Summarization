let articles = [];
let modernSummaries = [];
let classicSummaries = [];
let selectedArticle = null;
let currentModels = ["mt5", "gpt4"]; // İki model karşılaştırılacak: Sol ve sağ

// Başlangıçta verileri yükle
async function loadAllData() {
  const [articlesData, modernData, classicData] = await Promise.all([
    fetch("/uygulama/new-ui/data/articles.json").then(res => res.json()),
    fetch("data/merged_detailed.json").then(res => res.json()),
    fetch("data/classic_scores.json").then(res => res.json())
  ]);

  articles = articlesData;
  modernSummaries = modernData;
  classicSummaries = classicData;
  renderList();
}

function normalizeModelName(name) {
  const map = {
    gpt4: "chatgpt",
    mt5: "mt5",
    mbart: "mbart",
    llama: "llama"
  };
  return map[name] || name;
}

function getFirstSentence(text) {
  if (!text) return "";
  return text
    .replace(/\s+/g, " ")
    .replace(/[’‘”“"']/g, "")
    .split(/[.!?]/)[0]
    .trim()
    .toLowerCase();
}

function findModernSummary(articleText) {
  const norm = normalizeText(articleText);
  return modernSummaries.find(entry =>
    normalizeText(entry.article || "") === norm
  );
}
function findReferenceSummaryFromArticle(articleText) {
  const normArticle = normalizeText(articleText);
  const match = classicSummaries.find(entry =>
    normalizeText(entry.article || "") === normArticle
  );
  return match?.reference || null;
}

function normalizeText(text) {
  return text
    .toLowerCase()
    .replace(/[’‘”“"'.,:;!?]/g, "") // noktalama işaretlerini sil
    .replace(/\s+/g, " ")           // fazla boşlukları teke indir
    .trim();
}

function normalizeText(text) {
  return text
    .toLowerCase()
    .replace(/[’‘”“"'.,:;!?]/g, "")
    .replace(/\s+/g, " ")
    .trim();
}

function findClassicSummaryFromArticleText(articleText) {
  const target = normalizeText(articleText);
  return classicSummaries.find(entry =>
    normalizeText(entry.article || "") === target
  );
}
function findClassicScores(articleText, model) {
  const normArticle = normalizeText(articleText);
  const normModel = normalizeModelName(model);
  return classicSummaries.find(entry =>
    normalizeText(entry.summary) === normArticle && entry.model === normModel
  );
}



function formatMetricName(name) {
  const map = {
    rouge1: "ROUGE-1",
    rouge2: "ROUGE-2",
    rougeL: "ROUGE-L",
    bleu: "BLEU",
    bertscore_f1: "BERTScore (F1)",
    relevance: "Relevance",
    coherence: "Coherence",
    fluency: "Fluency",
    consistency: "Consistency",
    conciseness: "Conciseness",
    quotation_score: "Quotation Score",
    overall_score: "Overall Score"
  };
  return map[name] || name;
}

function toTitleCase(str) {
  return str
    .toLowerCase()
    .split(" ")
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");
}

function renderList() {
  const list = document.getElementById("articleList");
  list.innerHTML = "";
  articles.forEach((article, index) => {
    const firstSentence = getFirstSentence(article.original);
    const rawPreview = firstSentence.length > 40 
      ? firstSentence.slice(0, 40) + "..." 
      : firstSentence;

    const preview = toTitleCase(rawPreview);

    const item = document.createElement("li");
    item.textContent = `Article ${index + 1}: ${preview}`;
    item.addEventListener("click", () => showArticleDetails(article));
    list.appendChild(item);
  });
}


function showArticleDetails(article) {
const classic = findClassicSummaryFromArticleText(article.original);
console.log("🔍 Eşleşen classic:", classic);
console.log("🎯 Normalize:", normalizeText(article.original));

  selectedArticle = article;
  const details = document.getElementById("articleDetails");
//const classic = findClassicSummaryFromArticleText(article.original);
const modern = findModernSummary(article.original || article.article);
const originalSummary = article.summary || "Orijinal özet bulunamadı.";

  let html = `
    <h2>Article ${articles.indexOf(article) + 1}</h2>
    <p><strong>📰 Original:</strong> ${article.original}</p>
    <p><strong>📌 Original Summary:</strong> ${originalSummary}</p>

    <div style="display: flex; gap: 20px; flex-wrap: wrap;">
  `;

  currentModels.forEach((model, index) => {
    const modern = findModernSummary(article.original || article.article);
    const summary = modern?.[model]?.summary || "Bu modele ait özet bulunamadı.";
    const modernScores = modern?.[model]?.scores || {};
    const classicModelName = normalizeModelName(model);
const classicMatch = findClassicScores(summary, model);
const classicScores = classicMatch || {};

    html += `
      <div style="flex: 1; min-width: 300px; border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
        <h3>🔎 Choose a Model ${index + 1}:</h3>
        <select onchange="updateModel(${index}, this.value)">
          <option value="mt5" ${model === "mt5" ? "selected" : ""}>MT5</option>
          <option value="mbart" ${model === "mbart" ? "selected" : ""}>MBART</option>
          <option value="gpt4" ${model === "gpt4" ? "selected" : ""}>GPT-4</option>
          <option value="llama" ${model === "llama" ? "selected" : ""}>LLaMA</option>
        </select>

        <p><strong>✏️ Summary of the Model:</strong> ${summary}</p>

        <h4>📊 Modern Evulation Metrics </h4>
        <ul>
          ${
            Object.keys(modernScores).length > 0
              ? Object.entries(modernScores).map(([key, val]) => `<li>${formatMetricName(key)}: ${val ?? "null"}</li>`).join("")
              : "<li>Yok</li>"
          }
        </ul>

       <h4>📏 Classic Evulation Metrics</h4>
<ul>
  ${
    Object.keys(classicScores).length > 0
      ? Object.entries(classicScores)
          .filter(([key]) => ["rouge1", "rouge2", "rougeL", "bleu", "bertscore_f1"].includes(key))
          .map(([key, val]) => `<li>${formatMetricName(key)}: ${val.toFixed(3)}</li>`)
          .join("")
      : "<li>Yok</li>"
  }
</ul>

      </div>
    `;
  });

  html += `</div>`;
  html += `
  <div style="margin-top: 30px; padding: 10px; background: #f4f4f4; border-left: 4px solid #999;">
    <h4>ℹ️ Metric Explanation:</h4>
    <p><strong>Relevance</strong>: Whether the summary captures the key information.</p>
    <p><strong>Coherence</strong>: Logical and grammatical flow of the summary.</p>
    <p><strong>Consistency</strong>: Faithfulness to the original text without hallucination.</p>
    <p><strong>Fluency</strong>: Language quality and readability.</p>
    <p><strong>Conciseness</strong>: Avoidance of unnecessary length.</p>
    <p><strong>Quotation Score</strong>: Accuracy of quoted text.</p>
    <p><strong>Overall Score</strong>: General summary quality.</p>
    <br>
    <p><strong>ROUGE</strong>: Measures word overlap with reference summary.</p>
    <p><strong>BLEU</strong>: N-gram overlap metric from machine translation.</p>
    <p><strong>BERTScore (F1)</strong>: Semantic similarity between generated and reference summaries.</p>
  </div>
`;
  details.innerHTML = html;
}

// Model dropdown değişince çalışır
function updateModel(index, newModel) {
  currentModels[index] = newModel;
  if (selectedArticle) {
    showArticleDetails(selectedArticle); // yeniden çiz
  }
}

loadAllData();
