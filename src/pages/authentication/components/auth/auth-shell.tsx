import Link from "next/link"
import type { ReactNode } from "react"

export function AuthShell({
  title,
  subtitle,
  children,
  footer,
}: {
  title: string
  subtitle?: string
  children: ReactNode
  footer?: ReactNode
}) {
  return (
    <main className="min-h-dvh flex items-center justify-center px-4 py-10">
      <div className="w-full max-w-lg">
        <div className="mb-6 space-y-2 text-center">
          <span className="inline-block rounded-md border bg-secondary px-2 py-1 text-xs font-medium text-secondary-foreground">
            AI-Powered Environmental Intelligence
          </span>
          <h1 className="text-pretty text-2xl font-semibold tracking-tight">{title}</h1>
          {subtitle ? <p className="text-sm text-muted-foreground">{subtitle}</p> : null}
        </div>

        <div className="rounded-lg border bg-card p-6 shadow-sm">{children}</div>

        {footer ? (
          <div className="mt-6 text-center text-sm text-muted-foreground">{footer}</div>
        ) : (
          <div className="mt-6 text-center text-sm text-muted-foreground">
            By continuing, you agree to our{" "}
            <Link href="#" className="text-primary underline-offset-4 hover:underline">
              Terms
            </Link>{" "}
            and{" "}
            <Link href="#" className="text-primary underline-offset-4 hover:underline">
              Privacy Policy
            </Link>
            .
          </div>
        )}
      </div>
    </main>
  )
}
