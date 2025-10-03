import { AuthShell } from "@/components/auth/auth-shell"
import { SignupForm } from "@/components/auth/signup-form"

export default function Page() {
  return (
    <AuthShell
      title="Join AirAware"
      subtitle="Create your account to get real-time AQI, source attribution, and proactive health alerts." children={undefined}    >
      <SignupForm />
    </AuthShell>
  )
}
