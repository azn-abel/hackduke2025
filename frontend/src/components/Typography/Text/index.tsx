export default function Text({
  className,
  children,
}: Readonly<{
  className?: string;
  children: React.ReactNode;
}>) {
  return (
    <p
      className={`text-base font-[family-name:var(--font-geist-sans)] ${className}`}
    >
      {children}
    </p>
  );
}
