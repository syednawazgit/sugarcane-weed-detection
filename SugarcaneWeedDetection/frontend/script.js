async function uploadImage() {
  const fileInput = document.getElementById("fileInput");
  const file = fileInput.files[0];

  if (!file) {
    alert("Please select an image.");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  // Show loading text while waiting for prediction
  const loadingText = document.getElementById("loadingText");
  loadingText.textContent = "Detecting, please wait...";

  const response = await fetch("http://127.0.0.1:8000/predict/", {
    method: "POST",
    body: formData
  });

  if (response.ok) {
    const blob = await response.blob();
    const imageUrl = URL.createObjectURL(blob);

    // Find the result div and display the prediction result
    const resultDiv = document.getElementById("result");
    resultDiv.innerHTML = `<img src="${imageUrl}" alt="Prediction Result" style="max-width: 100%;"/>`;

    // Optionally hide loading text after displaying result
    loadingText.textContent = "";
  } else {
    alert("Prediction failed. Please try again.");
    const loadingText = document.getElementById("loadingText");
    loadingText.textContent = "";
  }
}
