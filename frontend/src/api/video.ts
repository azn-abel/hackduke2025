const API_URL = "http://127.0.0.1:5000";

async function uploadVideo(file: File): Promise<void> {
  if (!file) {
    console.error("No file selected.");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch(API_URL + "/upload-video/", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Upload failed: ${response.statusText}`);
    }

    const result = await response.json();
    console.log("Upload successful:", result);
  } catch (error) {
    console.error("Error uploading video:", error);
  }
}
