import Card from "@/components/Card";
import H2 from "@/components/Typography/Headings/H2";

export default function VideoCard({
  path,
  title,
}: {
  path: string;
  title?: string;
}) {
  return (
    <Card>
      <H2>{title || "Video"}</H2>
      <video src={path} controls className="max-w-96 max-h-96"></video>
    </Card>
  );
}
