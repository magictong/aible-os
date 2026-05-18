import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Aible OS",
  description: "Aible Operating System",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="h-full antialiased">
      <body className="h-full">{children}</body>
    </html>
  );
}