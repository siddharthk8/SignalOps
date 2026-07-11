import { AlertTriangle } from "lucide-react";

import Button from "@/components/Button";
import Container from "@/components/Container/Container";

function ErrorPage() {
	return (
		<div className="flex min-h-screen items-center justify-center bg-bg">
			<Container>
				<div className="mx-auto max-w-xl text-center">
					<div className="mt-2 flex justify-center">
						<div className="rounded-full bg-error/10 p-4">
							<AlertTriangle className="size-10 text-error" />
						</div>
					</div>

					<h1 className="mt-6 text-4xl font-bold text-t-primary">Something went wrong</h1>

					<p className="mx-auto mt-4 max-w-md text-lg text-t-muted">
						We're sorry, but an unexpected error occurred. Please try refreshing the
						page or come back in a few moments.
					</p>

					<Button onClick={() => (window.location.href = "/")} className="mt-8 mb-4 py-2">
						Go Home
					</Button>

					<p className="mt-8 text-sm text-t-muted">
						If the problem persists, please contact support.
					</p>
				</div>
			</Container>
		</div>
	);
}

export default ErrorPage;
