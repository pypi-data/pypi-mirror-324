"use client";

import * as React from "react";
import { ThemeProvider as NextThemesProvider } from "next-themes";
import { NuqsAdapter } from "nuqs/adapters/next/app";

import { SidebarProvider } from "@workspace/ui/components/sidebar";
export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <NextThemesProvider
      attribute="class"
      defaultTheme="system"
      enableSystem
      disableTransitionOnChange
      enableColorScheme
    >
      <NuqsAdapter>
        <SidebarProvider>{children}</SidebarProvider>
      </NuqsAdapter>
    </NextThemesProvider>
  );
}
