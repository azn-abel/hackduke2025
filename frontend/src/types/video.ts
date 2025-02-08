export interface Video {
  job_id: string;
  video_path: string;
}

export interface VideoData {
  raw: Array<Video>;
  processed: Array<Video>;
}
