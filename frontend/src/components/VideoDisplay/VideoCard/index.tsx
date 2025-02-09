import Card from "@/components/Card";
import H2 from "@/components/Typography/Headings/H2";
import Link from "next/link";

export default function VideoCard({
  path,
  title,
  job_id,
}: {
  path: string;
  title?: string;
  job_id: string;
}) {
  return (
    <Card>
      <H2>{title || "Video"}</H2>
      <video src={path} controls className="max-w-96"></video>
      <AnalyzeButton job_id={job_id} />
    </Card>
  );
}

function AnalyzeButton({ job_id }: { job_id: string }) {
  return (
    <Link
      href={"/video-analysis/" + job_id}
      className="rounded-full border border-solid border-transparent transition-colors flex items-center justify-center bg-foreground text-background gap-2 hover:bg-[#383838] dark:hover:bg-[#ccc] text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5 cursor-pointer"
    >
      Analyze Video
    </Link>
  );
}
