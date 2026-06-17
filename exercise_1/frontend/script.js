const imageInput = document.getElementById("imageInput");
const predictButton = document.getElementById("predictButton");
const preview = document.getElementById("preview");
const previewWrap = document.querySelector(".preview-wrap");
const resultLabel = document.querySelector(".result-label");
const apiUrlInput = document.getElementById("apiUrl");
const catScore = document.getElementById("catScore");
const dogScore = document.getElementById("dogScore");
const catBar = document.getElementById("catBar");
const dogBar = document.getElementById("dogBar");
const dropzone = document.querySelector(".dropzone");

const DEFAULT_API_URL = "https://golden-owl-demo.onrender.com";
apiUrlInput.value = DEFAULT_API_URL;

function formatPercent(value) {
  return `${Math.round(value * 100)}%`;
}

function setScores(scores = { cat: 0, dog: 0 }) {
  const cat = scores.cat || 0;
  const dog = scores.dog || 0;
  catScore.textContent = formatPercent(cat);
  dogScore.textContent = formatPercent(dog);
  catBar.style.width = formatPercent(cat);
  dogBar.style.width = formatPercent(dog);
}

imageInput.addEventListener("change", () => {
  const file = imageInput.files[0];
  predictButton.disabled = !file;
  setScores();
  resultLabel.textContent = file ? "Ready to classify" : "Waiting for image";

  if (!file) {
    preview.removeAttribute("src");
    previewWrap.classList.remove("has-image");
    dropzone.classList.remove("is-compact");
    return;
  }

  preview.src = URL.createObjectURL(file);
  previewWrap.classList.add("has-image");
  dropzone.classList.add("is-compact");
});

apiUrlInput.addEventListener("input", () => {
  localStorage.setItem("renderApiUrl", apiUrlInput.value.trim());
});

predictButton.addEventListener("click", async () => {
  const file = imageInput.files[0];
  const apiUrl = apiUrlInput.value.trim().replace(/\/$/, "");

  if (!file) {
    resultLabel.textContent = "Choose an image first";
    return;
  }

  if (!apiUrl) {
    resultLabel.textContent = "Enter your Render API URL";
    return;
  }

  const body = new FormData();
  body.append("file", file);

  predictButton.disabled = true;
  resultLabel.textContent = "Classifying...";

  try {
    const response = await fetch(`${apiUrl}/predict`, {
      method: "POST",
      body,
    });

    if (!response.ok) {
      const message = await response.text();
      throw new Error(message || `Request failed: ${response.status}`);
    }

    const data = await response.json();
    setScores(data.scores);
    resultLabel.textContent = `${data.prediction.toUpperCase()} - ${formatPercent(data.confidence)}`;
  } catch (error) {
    resultLabel.textContent = "Prediction failed";
    console.error(error);
  } finally {
    predictButton.disabled = false;
  }
});
