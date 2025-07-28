document.getElementById("pdfFile").addEventListener("change", async function (event) {
  event.preventDefault(); // ⛔ Prevent page refresh

  const file = event.target.files[0];
  if (!file || file.type !== "application/pdf") {
    alert("Please select a valid PDF file.");
    return;
  }

  // Show in Adobe Viewer
  const reader = new FileReader();
  reader.onload = function () {
    const base64PDF = reader.result;

    const adobeDCView = new AdobeDC.View({
      clientId: "68e726a72d654c7887ce27fca285ab78", // 🔁 Replace with your real Adobe PDF Embed API key
      divId: "adobe-dc-view",
    });

    adobeDCView.previewFile({
      content: {
        location: { url: base64PDF }
      },
      metaData: { fileName: file.name }
    }, {
      embedMode: "SIZED_CONTAINER"
    });
  };
  reader.readAsDataURL(file);

  // Send to backend
  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await fetch("http://localhost:5000/upload", {
      method: "POST",
      body: formData
    });

    const data = await res.json();
    if (data.error) {
      alert("Error: " + data.error);
    } else {
      document.getElementById("jsonOutput").innerText = JSON.stringify(data, null, 2);
    }
  } catch (err) {
    alert("Failed to send file: " + err.message);
  }
});
