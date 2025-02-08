export default function Card({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <article className="border p-4 rounded-lg font-[family-name:var(--font-geist-sans)]">
      {children}
    </article>
  );
}
