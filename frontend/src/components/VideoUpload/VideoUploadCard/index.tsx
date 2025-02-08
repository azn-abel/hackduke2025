"use client";

import Image from "next/image";
import Card from "@/components/Card";
import VideoUploadButton from "../VideoUploadButton";
import H2 from "@/components/Typography/Headings/H2";
import Text from "@/components/Typography/Text";
import { useState } from "react";

export default function VideoUploadCard() {
  const [fileName, setFileName] = useState("");

  return (
    <Card>
      <H2 className="text-center">Upload a Video</H2>
      <Text className="mb-4 text-center">Selected File: {fileName}</Text>
      <VideoUploadButton setter={setFileName} />
    </Card>
  );
}
