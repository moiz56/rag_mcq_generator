import type React from "react"
import type { Metadata } from "next"
import { Geist, Geist_Mono } from "next/font/google"
import { Analytics } from "@vercel/analytics/next"
import Link from "next/link"
import { Toaster } from "@/components/ui/sonner"
import "./globals.css"

const _geist = Geist({ subsets: ["latin"] })
const _geistMono = Geist_Mono({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "MCQ Generation Demo",
  description: "Generate multiple-choice questions using RAG",
  generator: "v0.app",
  icons: {
    icon: [
      {
        url: "/icon-light-32x32.png",
        media: "(prefers-color-scheme: light)",
      },
      {
        url: "/icon-dark-32x32.png",
        media: "(prefers-color-scheme: dark)",
      },
      {
        url: "/icon.svg",
        type: "image/svg+xml",
      },
    ],
    apple: "/apple-icon.png",
  },
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en" className="dark">
      <body className="font-sans antialiased min-h-screen flex flex-col bg-grid-pattern">
        {/* Animated background overlay */}
        <div className="fixed inset-0 pointer-events-none overflow-hidden">
          <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary/5 rounded-full blur-3xl animate-pulse-glow" />
          <div
            className="absolute bottom-1/4 right-1/4 w-80 h-80 bg-neon-purple/5 rounded-full blur-3xl animate-pulse-glow"
            style={{ animationDelay: "2s" }}
          />
        </div>

        <header className="border-b border-border/50 glass-card sticky top-0 z-50">
          <div className="container mx-auto px-4 h-16 flex items-center justify-between">
            <Link href="/" className="font-semibold text-lg hover:text-primary transition-colors tracking-wide">
              <span className="gradient-text">MCQ</span>
              <span className="text-muted-foreground ml-1">Generation</span>
            </Link>
            <div className="flex items-center gap-2 text-xs text-muted-foreground">
              <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
              <span>System Online</span>
            </div>
          </div>
        </header>
        <main className="flex-1 relative">{children}</main>
        <footer className="border-t border-border/50 py-6 mt-auto glass-card">
          {/* <div className="container mx-auto px-4 text-center text-sm text-muted-foreground">
            <span className="tracking-wide">Built with Next.js and RAG technology</span>
          </div> */}
        </footer>
        {/* <Toaster /> */}
        {/* <Analytics /> */}
      </body>
    </html>
  )
}
