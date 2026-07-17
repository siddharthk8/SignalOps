import { AlertTriangle } from "lucide-react";

import Button from "@/components/Button";
import Container from "@/components/Container/Container";

function ErrorPage() {
	return (
		<div className="bg-bg flex min-h-screen items-center justify-center">
			<Container>
				<div className="mx-auto max-w-xl text-center">
					<div className="mt-2 flex justify-center">
						<div className="bg-error/10 rounded-full p-4">
							<AlertTriangle className="text-error size-10" />
						</div>
					</div>

					<h1 className="text-t-primary mt-6 text-4xl font-bold">Something went wrong</h1>

					<p className="text-t-muted mx-auto mt-4 max-w-md text-lg">
						We're sorry, but an unexpected error occurred. Please try refreshing the
						page or come back in a few moments.
					</p>
					<Button onClick={() => (window.location.href = "/")} className="mt-8 mb-4 py-2">
						Go Home
					</Button>

					<p className="text-t-muted mt-8 text-sm">
						If the problem persists, please contact support.
					</p>
				</div>
			</Container>
		</div>
	);
}

export default ErrorPage;
