"use client";
import Image from "next/image";
import Card from "@/components/Card";
import H1 from "@/components/Typography/Headings/H1";
import H2 from "@/components/Typography/Headings/H2";
import { getVideo } from "@/api/video";
import { getAllVideos } from "@/api/video";
import { Job, VideoData } from "@/types/video";
import Text from "@/components/Typography/Text/";
import VideoUploadButton from "@/components/VideoUpload/VideoUploadButton";
import VideoUploadCard from "@/components/VideoUpload/VideoUploadCard";
import VideoCard from "@/components/VideoDisplay/VideoCard";
import VideoDisplay from "@/components/VideoDisplay";
import * as showdown from "showdown";

import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

export default function Page() {
  const params = useParams<{ id: string }>();
  const [videoData, setVideoData] = useState<Job | void>(undefined);
  const converter = new showdown.Converter();
  const fetchVideo = async (jobId: string) => {
    const data = await getVideo(jobId);
    if (data?.recommendation) {
      data.recommendation = converter.makeHtml(data.recommendation);
    }
    setVideoData(data);
    console.log(data);
  };

  useEffect(() => {
    fetchVideo(params.id);
  }, []);

  return (
    <>
      <H1 className="p-8 pt-24 text-3xl">Video Analysis</H1>
      <div className="flex flex-row justify-items-center min-h-screen p-8 pt-0 gap-16 font-[family-name:var(--font-geist-sans)]">
        <div className="flex flex-col gap-8 row-start-2 items-center sm:items-start">
          <Card className="w-96">
            <H2 className="text-2xl">Raw Video</H2>
            <video
              src={videoData?.video_path.substring(18)}
              controls
              className="w-96"
            />
          </Card>
          <Card className="w-96">
            <H2 className="text-4xl">Processed Video</H2>
            <video
              src={videoData?.processed_video_path.substring(18)}
              controls
              className="w-96"
            />
          </Card>
        </div>
        <div className="flex flex-col gap-4 row-start-2 items-center sm:items-start">
          <H2 className="text-3xl">Feedback</H2>
          <div
            dangerouslySetInnerHTML={{
              __html: videoData?.recommendation || "Nothing to show",
            }}
          ></div>
        </div>
      </div>
    </>
  );
}
