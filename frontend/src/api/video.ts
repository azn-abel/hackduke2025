import { VideoData } from "@/types/video";
import { Job } from "@/types/video";
const API_URL = "http://127.0.0.1:8000";

export async function uploadVideo(file: File): Promise<void> {
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

export async function getAllVideos(): Promise<VideoData | void> {
  try {
    const response = await fetch(API_URL + "/list-videos/", {
      method: "GET",
    });

    if (!response.ok) {
      throw new Error(`Fetch failed: ${response.statusText}`);
    }

    const result = await response.json();
    console.log("Fetch successful:", result);
    return result;
  } catch (error) {
    console.error("Error fetching videos:", error);
  }
}

export async function getVideo(jobId: string): Promise<Job | void> {
  try {
    const response = await fetch(API_URL + `/job/${jobId}/`, {
      method: "GET",
    });

    if (!response.ok) {
      throw new Error(`Fetch failed: ${response.statusText}`);
    }

    const result = await response.json();
    console.log("Fetch successful:", result);
    return result;
  } catch (error) {
    console.error("Error fetching video:", error);
  }
}
