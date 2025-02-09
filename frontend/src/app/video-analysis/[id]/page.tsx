"use client";
import Image from "next/image";
import Card from "@/components/Card";
import H2 from "@/components/Typography/Headings/H2";
import { getVideo } from "@/api/video";
import { getAllVideos } from "@/api/video";
import { Job, VideoData } from "@/types/video";
import Text from "@/components/Typography/Text/";
import VideoUploadButton from "@/components/VideoUpload/VideoUploadButton";
import VideoUploadCard from "@/components/VideoUpload/VideoUploadCard";
import VideoCard from "@/components/VideoDisplay/VideoCard";
import VideoDisplay from "@/components/VideoDisplay";

import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

export default function Page() {
  const params = useParams<{ id: string }>();
  const [videoData, setVideoData] = useState<Job | void>(undefined);
  const fetchVideo = async (jobId: string) => {
    const data = await getVideo(jobId);
    setVideoData(data);
    console.log(data);
  };
  useEffect(() => {
    fetchVideo(params.id);
  }, []);

  return (
    <div className="flex flex-row justify-items-center min-h-screen p-8 pt-24 gap-16 font-[family-name:var(--font-geist-sans)]">
      <p className="mt-20">Post: {params.id}</p>
      <main className="flex flex-col gap-4 row-start-2 items-center sm:items-start">
        <H2 className="text-4xl">Raw Video</H2>
        <video
          src={videoData?.video_path.substring(18)}
          controls
          className="max-w-96"
        ></video>
        <H2 className="text-4xl">Processed Video</H2>
        <video
          src={videoData?.processed_video_path.substring(18)}
          controls
          className="max-w-96"
        ></video>
      </main>
      <H2 className="text-4xl">Feedback</H2>
      <Text>{videoData?.recommendation}</Text>
    </div>
  );
}
