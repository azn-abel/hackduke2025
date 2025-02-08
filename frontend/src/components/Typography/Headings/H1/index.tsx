export default function H1({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <h1 className="text-2xl font-bold font-[family-name:var(--font-geist-sans)]">
      {children}
    </h1>
  );
}
