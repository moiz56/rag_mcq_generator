"use client"

import { FileText } from "lucide-react"
import type { MCQ } from "@/lib/types"
import { MCQAccordion } from "./mcq-accordion"

type Choice = "A" | "B" | "C" | "D"
type AnswersMap = Record<number, Choice | null>

interface MCQResultsProps {
  mcqs: MCQ[]
  isPlaceholder?: boolean
  hideAnswer?: boolean
  answers: AnswersMap
  onSelect: (index: number, choice: Choice) => void
  lockSelection?: boolean
}

export function MCQResults({
  mcqs,
  isPlaceholder = false,
  hideAnswer = true,
  answers,
  onSelect,
  lockSelection = false,
}: MCQResultsProps) {
  if (mcqs.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center h-64 text-center">
        <div className="p-4 rounded-full bg-secondary/30 mb-4">
          <FileText className="h-10 w-10 text-muted-foreground/50" />
        </div>
        <p className="text-muted-foreground">No MCQs available</p>
        <p className="text-sm text-muted-foreground/70">Generate MCQs to see results here</p>
      </div>
    )
  }

  return (
    <MCQAccordion
      mcqs={mcqs}
      isPlaceholder={isPlaceholder}
      hideAnswer={hideAnswer}
      answers={answers}
      onSelect={onSelect}
      lockSelection={lockSelection}
    />
  )
}
