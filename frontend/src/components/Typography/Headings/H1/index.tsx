export default function H1({
  children,
  className,
}: Readonly<{
  children: React.ReactNode;
  className?: string;
}>) {
  return (
    <h1
      className={`text-2xl font-bold font-[family-name:var(--font-geist-sans)] ${className}`}
    >
      {children}
    </h1>
  );
}
