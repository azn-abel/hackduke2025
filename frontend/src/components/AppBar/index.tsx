import Home from "../HomeButton";
import Link from "next/link";

export default function AppBar() {
  return (
    <nav className="bg-dukeblue content-center font-[family-name:var(--font-geist-sans)] fixed top-0 w-full">
      <Link href="/">
        <h1 className=" p-4 text-2xl font-bold cursor-pointer">ShotIQ</h1>
      </Link>
    </nav>
  );
}
