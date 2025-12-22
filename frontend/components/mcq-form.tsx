"use client"

import type React from "react"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Label } from "@/components/ui/label"
import { Loader2, Sparkles, Send, RotateCcw } from "lucide-react"
import { ProgressIndicator } from "./progress-indicator"

interface MCQFormProps {
  onGenerate: (text: string, numQuestions: number, difficulty: "easy" | "medium" | "hard") => void
  onSubmit: () => void
  onReset: () => void
  isLoading: boolean
  hasMCQs: boolean
  hasGenerated: boolean
}

export function MCQForm({ onGenerate, onSubmit, onReset, isLoading, hasMCQs, hasGenerated }: MCQFormProps) {
  const [text, setText] = useState("")
  const [numQuestions, setNumQuestions] = useState("5")
  const [difficulty, setDifficulty] = useState<"easy" | "medium" | "hard">("medium")

  const handleGenerate = (e: React.FormEvent) => {
    e.preventDefault()
    if (!text.trim()) return
    onGenerate(text, Number.parseInt(numQuestions), difficulty)
  }

  const handleReset = () => {
    setText("")
    onReset()
  }

  const currentStep: 1 | 2 | 3 = hasGenerated ? 3 : text.trim() ? 2 : 1

  return (
    <div className="space-y-6">
      <ProgressIndicator currentStep={currentStep} />

      <form onSubmit={handleGenerate} className="space-y-6">
        <div className="space-y-2">
          <Label htmlFor="text" className="text-sm tracking-wide">
            Paste text / topic / chapter
          </Label>
          <Textarea
            id="text"
            placeholder="Enter your study material, notes, or topic here..."
            value={text}
            onChange={(e) => setText(e.target.value)}
            disabled={isLoading}
            className="min-h-[180px] resize-y glass-card border-border/50 focus:border-primary/50 focus:neon-glow-subtle transition-all placeholder:text-muted-foreground/50"
            required
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-2">
            <Label htmlFor="num-questions" className="text-sm tracking-wide">
              Questions
            </Label>
            <Select value={numQuestions} onValueChange={setNumQuestions} disabled={isLoading}>
              <SelectTrigger id="num-questions" className="glass-card border-border/50">
                <SelectValue />
              </SelectTrigger>
              <SelectContent className="glass-card border-border/50">
                <SelectItem value="5">5 Questions</SelectItem>
                <SelectItem value="10">10 Questions</SelectItem>
                <SelectItem value="15">15 Questions</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label htmlFor="difficulty" className="text-sm tracking-wide">
              Difficulty
            </Label>
            <Select
              value={difficulty}
              onValueChange={(v) => setDifficulty(v as typeof difficulty)}
              disabled={isLoading}
            >
              <SelectTrigger id="difficulty" className="glass-card border-border/50">
                <SelectValue />
              </SelectTrigger>
              <SelectContent className="glass-card border-border/50">
                <SelectItem value="easy">Easy</SelectItem>
                <SelectItem value="medium">Medium</SelectItem>
                <SelectItem value="hard">Hard</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>

        <div className="space-y-3">
          <Button
            type="submit"
            className="w-full bg-primary hover:bg-primary/90 text-primary-foreground neon-glow-subtle hover:neon-glow transition-all"
            disabled={isLoading || !text.trim()}
          >
            {isLoading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Generating...
              </>
            ) : (
              <>
                <Sparkles className="mr-2 h-4 w-4" />
                Generate MCQs
              </>
            )}
          </Button>

          <div className="grid grid-cols-2 gap-3">
            <Button
              type="button"
              variant="secondary"
              onClick={onSubmit}
              disabled={!hasMCQs || isLoading}
              className="glass-card border border-border/50 hover:border-primary/50 hover:neon-glow-subtle transition-all"
            >
              <Send className="mr-2 h-4 w-4" />
              Submit
            </Button>
            <Button
              type="button"
              variant="outline"
              onClick={handleReset}
              disabled={isLoading}
              className="glass-card border border-border/50 hover:border-destructive/50 transition-all bg-transparent"
            >
              <RotateCcw className="mr-2 h-4 w-4" />
              Reset
            </Button>
          </div>
        </div>
      </form>
    </div>
  )
}
