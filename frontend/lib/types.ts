export interface MCQOption {
  A: string
  B: string
  C: string
  D: string
}

export interface MCQ {
  question: string
  options: MCQOption
  answer: "A" | "B" | "C" | "D"
  explanation?: string
  citation?: string
  isLatex?: boolean
}

export interface BackendMCQ {
  question: string
  A: string
  B: string
  C: string
  D: string
  correct: "A" | "B" | "C" | "D"
  citation: string
  explanation: string
  isLatex: boolean
}

export interface BackendMCQResponse {
  subject: string
  mcqs: BackendMCQ[]
}

export interface MCQResponse {
  subject: string
  mcqs: MCQ[]
}

function toFrontendMCQ(m: BackendMCQ): MCQ {
  return {
    question: m.question,
    options: { A: m.A, B: m.B, C: m.C, D: m.D },
    answer: m.correct,
    explanation: m.explanation,
    citation: m.citation,
    isLatex: m.isLatex,
  }
}

export function parseMCQResponse(data: unknown): MCQResponse {
  const raw = data as Partial<BackendMCQResponse>

  return {
    subject: raw.subject || "Unknown",
    mcqs: (raw.mcqs || []).map(toFrontendMCQ),
  }
}
