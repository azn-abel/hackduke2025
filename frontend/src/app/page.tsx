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
          <H2 className="text-4xl">Videos</H2>
          <VideoDisplay />
          <Image
            className="dark:invert"
            src="/next.svg"
            alt="Next.js logo"
            width={180}
            height={38}
            priority
          />

          <ol className="list-inside list-decimal text-sm text-center sm:text-left font-[family-name:var(--font-geist-mono)]">
            <li className="mb-2">
              Get started by editing{" "}
              <code className="bg-black/[.05] dark:bg-white/[.06] px-1 py-0.5 rounded font-semibold">
                src/app/page.tsx
              </code>
              .
            </li>
            <li>Save and see your changes instantly.</li>
          </ol>

          <div className="flex gap-4 items-center flex-col sm:flex-row">
            <a
              className="rounded-full border border-solid border-transparent transition-colors flex items-center justify-center bg-foreground text-background gap-2 hover:bg-[#383838] dark:hover:bg-[#ccc] text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5"
              href="https://vercel.com/new?utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
              target="_blank"
              rel="noopener noreferrer"
            >
              <Image
                className="dark:invert"
                src="/vercel.svg"
                alt="Vercel logomark"
                width={20}
                height={20}
              />
              Deploy now
            </a>
            <a
              className="rounded-full border border-solid border-black/[.08] dark:border-white/[.145] transition-colors flex items-center justify-center hover:bg-[#f2f2f2] dark:hover:bg-[#1a1a1a] hover:border-transparent text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5 sm:min-w-44"
              href="https://nextjs.org/docs?utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
              target="_blank"
              rel="noopener noreferrer"
            >
              Read our docs
            </a>
          </div>
        </main>
      </div>
    </>
  );
}
