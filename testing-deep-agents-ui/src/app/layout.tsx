import { Inter } from "next/font/google";
import { NuqsAdapter } from "nuqs/adapters/next/app";
import { Toaster } from "sonner";
import "./globals.css";
// NOTE  MC8yOmFIVnBZMlhtbkxIbXNaL210cHM2VFZadFRRPT06NWE4NzcyNzU=

const inter = Inter({ subsets: ["latin"] });

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html
      lang="zh-CN"
      suppressHydrationWarning
    >
      <body
        className={inter.className}
        suppressHydrationWarning
      >
        <NuqsAdapter>{children}</NuqsAdapter>
        <Toaster />
      </body>
    </html>
  );
}
// @ts-expect-error  MS8yOmFIVnBZMlhtbkxIbXNaL210cHM2VFZadFRRPT06NWE4NzcyNzU=
