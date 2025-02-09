import Home from "../HomeButton";
import Link from "next/link";
import Image from "next/image";

export default function AppBar() {
  return (
    <nav className="bg-dukeblue content-center font-[family-name:var(--font-geist-sans)] fixed top-0 w-full">
      <Link href="/">
        <img
          className="p-4 text-2xl font-bold cursor-pointer h-16"
          src="/logo.png"
          alt="logo"
        />
      </Link>
    </nav>
  );
}
