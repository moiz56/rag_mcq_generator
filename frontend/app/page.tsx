"use client"

import Link from "next/link"
import { Calculator, Atom, BookOpen, ArrowRight } from "lucide-react"
import { useEffect, useState } from "react"

const subjects = [
  {
    name: "Maths",
    slug: "maths",
    tagline: "Algebra, Geometry & Calculus",
    icon: Calculator,
  },
  {
    name: "Physics",
    slug: "physics",
    tagline: "Forces, Energy & Circuits",
    icon: Atom,
  },
  {
    name: "English",
    slug: "english",
    tagline: "Grammar, Vocab & Comprehension",
    icon: BookOpen,
  },
]

export default function HomePage() {
  const [pingStatus, setPingStatus] = useState<"checking" | "connected" | "failed">("checking")
  const [pingMessage, setPingMessage] = useState<string>("")

  useEffect(() => {
    const run = async () => {

      const base = process.env.NEXT_PUBLIC_API_BASE_URL;
      
      try {
        const res = await fetch(`${base}/ping`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        const data = await res.json()
        setPingStatus("connected")
        setPingMessage(data?.message ?? "pong")
      } catch (e: any) {
        setPingStatus("failed")
        setPingMessage(e?.message ?? "Failed to connect")
      }
    }
    run()
  }, [])

  return (
    <div className="container mx-auto px-4 py-16 relative">
      <div className="text-center mb-16">
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass-card border border-border/50 mb-8">
          <div
            className={[
              "w-2 h-2 rounded-full",
              pingStatus === "checking" ? "bg-yellow-500 animate-pulse" : "",
              pingStatus === "connected" ? "bg-emerald-500" : "",
              pingStatus === "failed" ? "bg-red-500" : "",
            ].join(" ")}
          />
          <span className="text-xs text-muted-foreground tracking-wide">
            {" "}
            {pingStatus === "checking"
              ? "Checking..."
              : pingStatus === "connected"
              ? `Connected `
              : `Not connected `}
          </span>
        </div>

        <h1 className="text-5xl md:text-6xl font-bold tracking-tight mb-6">
          <span className="gradient-text">RAG - Based MCQ Generation</span>
        </h1>

        <p className="text-xl text-muted-foreground max-w-2xl mx-auto mb-4 leading-relaxed">
          Generate multiple-choice questions to help YOU prepare for your entry test exams
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl mx-auto">
        {subjects.map((subject) => (
          <Link key={subject.slug} href={`/mcq/${subject.slug}`} className="group">
            <div className="h-full glass-card rounded-xl border border-border/50 p-8 hover:border-primary/50 hover:neon-glow transition-all duration-300 transform hover:-translate-y-1">
              <div className="flex flex-col items-center text-center">
                <div className="mb-6 p-4 rounded-xl bg-primary/10 group-hover:bg-primary/20 transition-colors neon-glow-subtle">
                  <subject.icon className="h-10 w-10 text-primary" />
                </div>

                <h2 className="text-2xl font-semibold mb-2 tracking-wide group-hover:text-primary transition-colors">
                  {subject.name}
                </h2>

                <p className="text-sm text-muted-foreground mb-6">{subject.tagline}</p>

                <div className="flex items-center gap-2 text-sm text-primary opacity-0 group-hover:opacity-100 transition-opacity">
                  <span className="tracking-wide">Enter</span>
                  <ArrowRight className="h-4 w-4 group-hover:translate-x-1 transition-transform" />
                </div>
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  )
}
