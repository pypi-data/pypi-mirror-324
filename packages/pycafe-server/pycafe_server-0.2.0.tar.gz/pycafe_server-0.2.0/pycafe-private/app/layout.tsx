"use client";
import "@/app/globals.css";
import { Inter } from "next/font/google";
import AutoTheme from "@/app/components/AutoTheme";
// import { Analytics } from "@vercel/analytics/react";
import { AppRouterCacheProvider } from "@mui/material-nextjs/v13-appRouter";
import { UserAndSettingsProvider } from "@/components/user-server";

const inter = Inter({ subsets: ["latin"] });

// const title = `PyCafe: ${tagline}`;
// const description = "Playground for Python web frameworks. Run and edit Python code snippets for web frameworks in a web browser.";

// export const metadata = {
//   title,
//   description,
// };

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <AppRouterCacheProvider>
      <AutoTheme>
        <html lang="en">
          <body
            suppressHydrationWarning={true}
            className={inter.className}
            style={{ display: "flex", flexDirection: "column", minHeight: "100vh" }}
          >
            <UserAndSettingsProvider>{children}</UserAndSettingsProvider>
            {/* <Analytics /> */}
          </body>
        </html>
      </AutoTheme>
    </AppRouterCacheProvider>
  );
}
