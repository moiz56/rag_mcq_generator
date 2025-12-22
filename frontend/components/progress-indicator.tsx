"use client"

interface ProgressIndicatorProps {
  currentStep: 1 | 2 | 3
}

const steps = [
  { number: 1, label: "Input" },
  { number: 2, label: "Generate" },
  { number: 3, label: "Submit" },
]

export function ProgressIndicator({ currentStep }: ProgressIndicatorProps) {
  return (
    <div className="flex items-center justify-between mb-6">
      {steps.map((step, index) => (
        <div key={step.number} className="flex items-center flex-1">
          <div className="flex items-center gap-2">
            <div
              className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-mono transition-all ${
                step.number <= currentStep
                  ? "bg-primary text-primary-foreground neon-glow-subtle"
                  : "bg-secondary/50 text-muted-foreground border border-border/50"
              }`}
            >
              {step.number}
            </div>
            <span
              className={`text-xs tracking-wide ${
                step.number <= currentStep ? "text-primary" : "text-muted-foreground"
              }`}
            >
              {step.label}
            </span>
          </div>
          {index < steps.length - 1 && (
            <div className={`flex-1 h-px mx-3 ${step.number < currentStep ? "bg-primary/50" : "bg-border/50"}`} />
          )}
        </div>
      ))}
    </div>
  )
}
