export default function Card({
  children,
  className,
}: Readonly<{
  children: React.ReactNode;
  className?: string;
}>) {
  return (
    <article
      className={`border p-4 rounded-lg font-[family-name:var(--font-geist-sans)] ${className}`}
    >
      {children}
    </article>
  );
}
