import type { MCQ } from "./types"

export const placeholderMCQs: Record<string, MCQ[]> = {
  maths: [
    {
      question: "What is the value of x in the equation 2x + 5 = 15?",
      options: { A: "3", B: "5", C: "7", D: "10" },
      answer: "B",
      explanation: "Subtract 5 from both sides: 2x = 10. Divide by 2: x = 5.",
    },
    {
      question: "What is the area of a circle with radius 7 units? (Use π = 22/7)",
      options: { A: "44 sq units", B: "154 sq units", C: "88 sq units", D: "308 sq units" },
      answer: "B",
      explanation: "Area = πr² = (22/7) × 7² = (22/7) × 49 = 154 sq units.",
    },
    {
      question: "What is the derivative of f(x) = 3x² + 2x - 1?",
      options: { A: "6x + 2", B: "3x + 2", C: "6x² + 2", D: "6x - 1" },
      answer: "A",
      explanation: "Using the power rule: d/dx(3x²) = 6x, d/dx(2x) = 2, d/dx(-1) = 0. So f'(x) = 6x + 2.",
    },
  ],
  physics: [
    {
      question: "According to Newton's First Law, an object at rest will:",
      options: {
        A: "Always start moving eventually",
        B: "Remain at rest unless acted upon by an external force",
        C: "Move in a circular path",
        D: "Accelerate downward",
      },
      answer: "B",
      explanation:
        "Newton's First Law (Law of Inertia) states that an object will maintain its state of rest or uniform motion unless acted upon by an external force.",
    },
    {
      question: "What is the SI unit of electrical resistance?",
      options: { A: "Ampere", B: "Volt", C: "Ohm", D: "Watt" },
      answer: "C",
      explanation: "The SI unit of electrical resistance is the Ohm (Ω), named after Georg Ohm.",
    },
    {
      question: "Kinetic energy is calculated using which formula?",
      options: { A: "KE = mgh", B: "KE = ½mv²", C: "KE = Fd", D: "KE = mv" },
      answer: "B",
      explanation: "Kinetic energy equals one-half times mass times velocity squared: KE = ½mv².",
    },
  ],
  english: [
    {
      question: "Which word is a synonym for 'benevolent'?",
      options: { A: "Malicious", B: "Indifferent", C: "Kind", D: "Hostile" },
      answer: "C",
      explanation: "'Benevolent' means well-meaning and kind, making 'kind' the correct synonym.",
    },
    {
      question: "Identify the correct sentence:",
      options: {
        A: "Their going to the store.",
        B: "There going to the store.",
        C: "They're going to the store.",
        D: "Theyre going to the store.",
      },
      answer: "C",
      explanation: "'They're' is the contraction of 'they are', which is correct in this context.",
    },
    {
      question: "What literary device is used in 'The wind whispered through the trees'?",
      options: { A: "Metaphor", B: "Simile", C: "Personification", D: "Hyperbole" },
      answer: "C",
      explanation:
        "Personification gives human qualities to non-human things. Here, the wind is given the human ability to whisper.",
    },
  ],
}
