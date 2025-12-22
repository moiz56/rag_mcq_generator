"use client"

import { useState } from "react"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { MCQForm } from "@/components/mcq-form"
import { MCQResults } from "@/components/mcq-results"
import { BreadcrumbNav } from "@/components/breadcrumb-nav"
import { parseMCQResponse, type MCQ } from "@/lib/types"
import { placeholderMCQs } from "@/lib/placeholders"
import { ArrowLeft, AlertCircle, Sparkles } from "lucide-react"
import { toast } from "sonner"
import Link from "next/link"

const base = process.env.NEXT_PUBLIC_API_BASE_URL;


type Choice = "A" | "B" | "C" | "D"
type AnswersMap = Record<number, Choice | null>

const subjectEndpoints: Record<string, string> = {
  maths: `${base}/mcq_math`,
  physics: `${base}/mcq_physic`,
  english: `${base}/mcq_english`,
}

interface MCQPageClientProps {
  subject: string
}

export function MCQPageClient({ subject }: MCQPageClientProps) {
  const [mcqs, setMcqs] = useState<MCQ[]>(placeholderMCQs[subject] || [])
  const [isPlaceholder, setIsPlaceholder] = useState(true)
  const [hideAnswer, setHideAnswer] = useState(true)
  const [isLoading, setIsLoading] = useState(false)
  const [hasGenerated, setHasGenerated] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [answers, setAnswers] = useState<AnswersMap>({})
  const [submitted, setSubmitted] = useState(false)
  const [score, setScore] = useState<{ correct: number; total: number } | null>(null)
  const formattedSubject = subject.charAt(0).toUpperCase() + subject.slice(1)

  const handleSelect = (index: number, choice: Choice) => {
  if (submitted) return
  setAnswers((prev) => ({ ...prev, [index]: choice }))
}

const handleGenerateMCQs = async (
  text: string,
  numQuestions: number,
  difficulty: "easy" | "medium" | "hard"
) => {
  setAnswers({})
  setSubmitted(false)
  setScore(null)
  setHideAnswer(true)
  setIsLoading(true)
  setError(null)

  try {
    const endpoint = subjectEndpoints[subject]
    if (!endpoint) throw new Error(`Unknown subject: ${subject}`)
    if (!base) throw new Error("NEXT_PUBLIC_API_BASE_URL is not set")

    const response = await fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        query: text,
        difficulty,
        num_questions: numQuestions,
      }),
    })

    if (!response.ok) {
      const body = await response.text().catch(() => "")
      throw new Error(`API error: ${response.status} ${response.statusText}${body ? ` - ${body}` : ""}`)
    }

    const data = await response.json()
    const parsed = parseMCQResponse(data)

    setMcqs(parsed.mcqs)
    setIsPlaceholder(false)
    setHasGenerated(true)

    toast.success("MCQs Generated", {
      description: `Successfully generated ${parsed.mcqs.length} questions.`,
    })
  } catch (err) {
    const msg = err instanceof Error ? err.message : "Failed to generate MCQs. Please try again."
    setError(msg)
    toast.error("Generation Failed", { description: msg })
  } finally {
    setIsLoading(false)
  }
}


  const handleSubmit = () => {
  if (mcqs.length === 0) {
    toast.error("No MCQs to submit", { description: "Generate or use demo MCQs first." })
    return
  }

  const unanswered = mcqs.some((_, i) => !answers[i])
  if (unanswered) {
    toast.error("Please answer all questions", { description: "You left some MCQs unanswered." })
    return
  }

  const correct = mcqs.reduce((acc, q, i) => acc + (answers[i] === q.answer ? 1 : 0), 0)
  const total = mcqs.length

  setSubmitted(true)
  setScore({ correct, total })
  setHideAnswer(false) 

  toast.success("Submitted", { description: `Score: ${correct}/${total}` })
}


const handleReset = () => {
  setMcqs(placeholderMCQs[subject] || [])
  setIsPlaceholder(true)
  setHasGenerated(false)
  setError(null)

  setAnswers({})
  setSubmitted(false)
  setScore(null)
  setHideAnswer(true)
}

  return (
    <div className="container mx-auto px-4 py-8">
      <BreadcrumbNav subject={subject} />

      <div className="flex items-center gap-4 mb-8">
        <Button variant="ghost" size="sm" asChild className="hover:bg-secondary/50">
          <Link href="/">
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back
          </Link>
        </Button>
      </div>

      <div className="mb-8">
        <div className="flex items-center gap-3 mb-3">
          <Badge variant="outline" className="border-primary/50 text-primary px-3 py-1 neon-glow-subtle">
            {formattedSubject}
          </Badge>
        </div>
        <h1 className="text-3xl font-bold tracking-wide mb-2">
          <span className="gradient-text">Generate MCQs</span>
        </h1>
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <Sparkles className="h-4 w-4 text-primary" />
          <span>RAG-powered MCQ generation</span>
        </div>
        <div className="mt-4 h-px w-32 bg-gradient-to-r from-primary/80 to-transparent" />
      </div>

      {error && (
        <Alert variant="destructive" className="mb-6 glass-card border-destructive/50">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      <div className="grid lg:grid-cols-2 gap-8">
        <div className="glass-card rounded-xl border border-border/50 p-6">
          <h2 className="text-lg font-semibold mb-6 tracking-wide text-foreground/90">Input</h2>
          <MCQForm
            onGenerate={handleGenerateMCQs}
            onSubmit={handleSubmit}
            onReset={handleReset}
            isLoading={isLoading}
            hasMCQs={mcqs.length > 0}
            hasGenerated={hasGenerated}
          />
        </div>

        <div className="glass-card rounded-xl border border-border/50 p-6">
          <h2 className="text-lg font-semibold mb-6 tracking-wide text-foreground/90">
            {isPlaceholder ? "Demo MCQs" : "Generated MCQs"}
          </h2>
              {score && (
              <Badge variant="outline" className="border-primary/50 text-primary px-3 py-1 neon-glow-subtle">
                Score: {score.correct}/{score.total}
              </Badge>
            )}
          <MCQResults
              mcqs={mcqs}
              isPlaceholder={isPlaceholder}
              hideAnswer={hideAnswer}
              answers={answers}
              onSelect={handleSelect}
              lockSelection={submitted}
            />
        </div>
      </div>
    </div>
  )
}
