export default function Card({
  children,
  className,
}: Readonly<{
  children: React.ReactNode;
  className?: string;
}>) {
  return (
    <article
      className={`p-4 rounded-lg font-[family-name:var(--font-geist-sans)] bg-[#1E1E1E] ${className}`}
    >
      {children}
    </article>
  );
}
