import { AuthShell } from "@/components/auth/auth-shell"
import { LoginForm } from "@/components/auth/login-form"

export default function Page() {
  return (
    <AuthShell
      title="Breathe easy. Sign in"
      subtitle="Access live air quality insights, policy analytics, and personalized health recommendations." children={undefined}    >
      <LoginForm />
    </AuthShell>
  )
}
