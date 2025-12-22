"use client"

import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Copy, Check } from "lucide-react"
import { useState } from "react"
import type { MCQ } from "@/lib/types"

type Choice = "A" | "B" | "C" | "D"
type AnswersMap = Record<number, Choice | null>

interface MCQAccordionProps {
  mcqs: MCQ[]
  isPlaceholder?: boolean
  hideAnswer?: boolean

  answers: AnswersMap
  onSelect: (index: number, choice: Choice) => void
  lockSelection?: boolean
}

export function MCQAccordion({
  mcqs,
  isPlaceholder = false,
  hideAnswer = true,
  answers,
  onSelect,
  lockSelection = false,
}: MCQAccordionProps) {
  const [copiedJson, setCopiedJson] = useState(false)
  const [copiedText, setCopiedText] = useState(false)

  const copyAsJson = async () => {
    await navigator.clipboard.writeText(JSON.stringify(mcqs, null, 2))
    setCopiedJson(true)
    setTimeout(() => setCopiedJson(false), 2000)
  }

  const copyAsText = async () => {
    const textContent = mcqs
      .map((mcq, i) => {
        const lines = [
          `Q${i + 1}: ${mcq.question}`,
          `A) ${mcq.options.A}`,
          `B) ${mcq.options.B}`,
          `C) ${mcq.options.C}`,
          `D) ${mcq.options.D}`,
        ]

        // Only include answer/explanation/citation if not hidden
        if (!hideAnswer) {
          lines.push(`Answer: ${mcq.answer}`)
          if (mcq.explanation) lines.push(`Explanation: ${mcq.explanation}`)
          if (mcq.citation) lines.push(`Citation: ${mcq.citation}`)
        }

        return lines.join("\n")
      })
      .join("\n\n")

    await navigator.clipboard.writeText(textContent)
    setCopiedText(true)
    setTimeout(() => setCopiedText(false), 2000)
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        {isPlaceholder && (
          <Badge variant="outline" className="border-primary/50 text-primary text-xs">
            Demo MCQs
          </Badge>
        )}

        <div className="flex gap-2 ml-auto">
          <Button
            variant="outline"
            size="sm"
            onClick={copyAsJson}
            className="glass-card border-border/50 hover:border-primary/50 hover:neon-glow-subtle transition-all bg-transparent"
          >
            {copiedJson ? <Check className="mr-2 h-4 w-4 text-emerald-400" /> : <Copy className="mr-2 h-4 w-4" />}
            JSON
          </Button>

          <Button
            variant="outline"
            size="sm"
            onClick={copyAsText}
            className="glass-card border-border/50 hover:border-primary/50 hover:neon-glow-subtle transition-all bg-transparent"
          >
            {copiedText ? <Check className="mr-2 h-4 w-4 text-emerald-400" /> : <Copy className="mr-2 h-4 w-4" />}
            Text
          </Button>
        </div>
      </div>

      <Accordion type="multiple" className="space-y-3">
        {mcqs.map((mcq, index) => (
          <AccordionItem
            key={index}
            value={`item-${index}`}
            className="glass-card border border-border/50 rounded-lg px-4 hover:border-primary/30 transition-colors"
          >
            <AccordionTrigger className="hover:no-underline py-4">
              <span className="text-left">
                <span className="font-mono text-primary mr-3">Q{index + 1}</span>
                <span className="text-foreground/90">{mcq.question}</span>
              </span>
            </AccordionTrigger>

            <AccordionContent className="space-y-3 pt-2 pb-4">
              <div className="grid gap-2">
              {(["A", "B", "C", "D"] as const).map((key) => {
  const picked = answers[index] ?? null
  const isPicked = picked === key
  const isCorrect = mcq.answer === key

  return (
    <button
      key={key}
      type="button"
      disabled={lockSelection}
      onClick={() => onSelect(index, key)}
      className={`w-full text-left p-3 rounded-lg border transition-all ${
        // after submit
        !hideAnswer && isCorrect
          ? "bg-emerald-500/10 border-emerald-500/50 text-emerald-300 neon-glow-subtle"
          : !hideAnswer && isPicked && !isCorrect
          ? "bg-destructive/10 border-destructive/50 text-destructive"
          // before submit
          : isPicked
          ? "bg-primary/10 border-primary/40"
          : "bg-secondary/30 border-border/30 text-foreground/80"
      } ${lockSelection ? "cursor-not-allowed opacity-90" : "hover:border-primary/40"}`}
    >
      <span className="font-mono font-medium mr-3 text-primary/80">{key}</span>
      {mcq.options[key]}

      {/* Before submit */}
      {hideAnswer && isPicked && (
        <Badge className="ml-3 bg-primary/20 text-primary border-primary/30">
          Selected
        </Badge>
      )}

      {/* After submit */}
      {!hideAnswer && isCorrect && (
        <Badge className="ml-3 bg-emerald-500/20 text-emerald-300 border-emerald-500/30">
          Correct
        </Badge>
      )}
      {!hideAnswer && isPicked && !isCorrect && (
        <Badge className="ml-3 bg-destructive/20 text-destructive border-destructive/30">
          Your choice
        </Badge>
      )}
    </button>
  )
})}    
              </div>

              {/* Explanation */}
              {!hideAnswer && mcq.explanation && (
                <div className="mt-4 p-4 glass-card rounded-lg border-primary/20">
                  <p className="text-xs font-medium text-primary mb-2 tracking-wide uppercase">Explanation</p>
                  <p className="text-sm text-muted-foreground leading-relaxed">{mcq.explanation}</p>
                </div>
              )}

              {/* Citation */}
              {hideAnswer && mcq.citation && (
                <div className="mt-3 p-4 glass-card rounded-lg border-primary/20">
                  <p className="text-xs font-medium text-primary mb-2 tracking-wide uppercase">Citation</p>
                  <p className="text-sm text-muted-foreground leading-relaxed break-words">{mcq.citation}</p>
                </div>
              )}
            </AccordionContent>
          </AccordionItem>
        ))}
      </Accordion>
    </div>
  )
}
