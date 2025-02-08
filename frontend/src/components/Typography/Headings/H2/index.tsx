export default function H2({
  className,
  children,
}: Readonly<{
  className?: string;
  children: React.ReactNode;
}>) {
  return (
    <h2
      className={`text-xl mb-2 font-bold font-[family-name:var(--font-geist-sans)] ${className}`}
    >
      {children}
    </h2>
  );
}
