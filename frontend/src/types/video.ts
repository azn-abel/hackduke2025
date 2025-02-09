export interface Video {
  job_id: string;
  video_path: string;
}

export interface VideoData {
  raw: Array<Video>;
  processed: Array<Video>;
}

export interface Job {
  video_filename: string;
  status: string;
  video_path: string;
  processed_video_path: string;
  recommendation: string;
}
