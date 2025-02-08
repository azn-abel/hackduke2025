import H2 from "../Typography/Headings/H2";
import VideoCard from "./VideoCard";

interface VideoData {
  raw: Array<string>;
  processed: Array<string>;
}

export default function VideoDisplay({ data }: { data: VideoData }) {
  return (
    <>
      <H2>Raw Footage</H2>
      <VideoBox>
        {data.raw.map((path, i) => {
          return <VideoCard path={path} key={i} />;
        })}
      </VideoBox>

      <H2>Processed Footage Footage</H2>
      <VideoBox>
        {data.processed.length > 0
          ? data.processed.map((path, i) => {
              return <VideoCard path={path} key={i} />;
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
