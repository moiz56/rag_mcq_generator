import Link from "next/link"
import { ChevronRight, Home } from "lucide-react"

interface BreadcrumbNavProps {
  subject: string
}

export function BreadcrumbNav({ subject }: BreadcrumbNavProps) {
  const formattedSubject = subject.charAt(0).toUpperCase() + subject.slice(1)

  return (
    <nav className="flex items-center gap-2 text-sm text-muted-foreground mb-6">
      <Link href="/" className="flex items-center hover:text-primary transition-colors">
        <Home className="h-4 w-4" />
      </Link>
      <ChevronRight className="h-4 w-4 text-border" />
      <span>MCQ</span>
      <ChevronRight className="h-4 w-4 text-border" />
      <span className="text-primary font-medium">{formattedSubject}</span>
    </nav>
  )
}
