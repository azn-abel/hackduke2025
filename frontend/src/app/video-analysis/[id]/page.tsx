"use client";
import Image from "next/image";
import Card from "@/components/Card";
import H2 from "@/components/Typography/Headings/H2";
import Text from "@/components/Typography/Text/";
import VideoUploadButton from "@/components/VideoUpload/VideoUploadButton";
import VideoUploadCard from "@/components/VideoUpload/VideoUploadCard";
import VideoCard from "@/components/VideoDisplay/VideoCard";
import VideoDisplay from "@/components/VideoDisplay";

import { useParams } from "next/navigation";

export default function Page() {
  const params = useParams<{ id: string }>();

  return (
    <div className="flex flex-row justify-items-center min-h-screen p-8 pt-24 gap-16 font-[family-name:var(--font-geist-sans)]">
      <p className="mt-20">Post: {params.id}</p>
      <main className="flex flex-col gap-4 row-start-2 items-center sm:items-start">
        <H2 className="text-4xl">Videos</H2>
        <VideoDisplay />
      </main>
      <H2 className="text-4xl">Feedback</H2>
    </div>
  );
}
