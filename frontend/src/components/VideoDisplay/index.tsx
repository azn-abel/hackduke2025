import H2 from "../Typography/Headings/H2";
import VideoCard from "./VideoCard";
import { getAllVideos } from "@/api/video";
import { VideoData } from "@/types/video";

export default async function VideoDisplay() {
  const data: VideoData | void = await getAllVideos();

  console.log(data);

  return (
    <>
      <H2>Raw Footage</H2>
      <VideoBox>
        {data?.raw.map((path, i) => {
          return <VideoCard path={"/videos/raw/" + path} key={i} />;
        })}
      </VideoBox>

      <H2>Processed Footage Footage</H2>
      <VideoBox>
        {data && data.processed.length > 0
          ? data?.processed.map((path, i) => {
              return <VideoCard path={"/videos/processed/" + path} key={i} />;
            })
          : "No videos to show."}
      </VideoBox>
    </>
  );
}

function VideoBox({ children }: { children?: React.ReactNode }) {
  return (
    <div className="flex flex-row flex-wrap gap-8">
      {children || "No videos to show."}
    </div>
  );
}
