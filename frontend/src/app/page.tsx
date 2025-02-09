import Image from "next/image";
import Card from "@/components/Card";
import H2 from "@/components/Typography/Headings/H2";
import Text from "@/components/Typography/Text/";
import VideoUploadButton from "@/components/VideoUpload/VideoUploadButton";
import VideoUploadCard from "@/components/VideoUpload/VideoUploadCard";
import VideoCard from "@/components/VideoDisplay/VideoCard";
import VideoDisplay from "@/components/VideoDisplay";

export default function Home() {
  return (
    <>
      <div className="flex flex-row justify-items-center min-h-screen p-8 pt-24 gap-16 font-[family-name:var(--font-geist-sans)]">
        <aside className="min-w-5xl">
          <VideoUploadCard />
        </aside>
        <main className="flex flex-col gap-4 row-start-2 items-center sm:items-start">
          <H2 className="text-3xl">Videos</H2>
          <VideoDisplay />
        </main>
      </div>
    </>
  );
}
