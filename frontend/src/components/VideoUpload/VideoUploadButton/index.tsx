"use client";

import Image from "next/image";
import { Dispatch, ChangeEvent, SetStateAction, useState } from "react";
import { uploadVideo } from "@/api/video";

export default function VideoUploadButton({
  setter,
}: {
  setter: Dispatch<SetStateAction<string>>;
}) {
  const [file, setFile] = useState<File | null>();

  const useSetter = (e: ChangeEvent<HTMLInputElement>) => {
    const fileName: string = e.target.value;
    const array = fileName.split("\\");
    const file = array[array.length - 1];
    setter(file);
    if (e.target.files && e.target.files.length > 0) {
      console.log("uploading");
      uploadVideo(e.target.files[0]);
    }
  };

  return (
    <label
      htmlFor="video-upload-button"
      className="rounded-full border border-solid border-transparent transition-colors flex items-center justify-center bg-foreground text-background gap-2 hover:bg-[#383838] dark:hover:bg-[#ccc] text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5 cursor-pointer"
      onClick={() => {
        console.log("ello");
      }}
    >
      <Image
        className="dark:invert"
        src="/vercel.svg"
        alt="Vercel logomark"
        width={20}
        height={20}
      />
      <input id="video-upload-button" type="file" onChange={useSetter} hidden />
      Choose a File
    </label>
  );
}
