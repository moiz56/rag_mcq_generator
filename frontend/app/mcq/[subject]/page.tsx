"use client"
import { notFound } from "next/navigation"
import { MCQPageClient } from "./mcq-page-client"

const validSubjects = ["maths", "physics", "english"]

export default async function MCQPage({ params }: { params: Promise<{ subject: string }> }) {
  const { subject } = await params

  if (!validSubjects.includes(subject)) {
    notFound()
  }

  return <MCQPageClient subject={subject} />
}
