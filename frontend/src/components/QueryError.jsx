import { WifiOff } from "lucide-react";

import Button from "@/components/Button";
import Container from "@/components/Container";

function QueryError({
	title = "Failed to load data",
	message = "We couldn't retrieve the requested information. Please try again.",
	onRetry,
}) {
	return (
		<Container>
			<div className="border-border bg-surface rounded-2xl border p-8 shadow-sm">
				<div className="flex flex-col items-center text-center">
					<div className="bg-error/10 mb-5 flex size-14 items-center justify-center rounded-full">
						<WifiOff className="text-error size-7" />
					</div>

					<h3 className="text-t-primary text-xl font-semibold">{title}</h3>

					<p className="text-t-muted mt-2 max-w-md">{message}</p>

					<Button onClick={onRetry} className="mt-6">
						Retry
					</Button>
				</div>
			</div>
		</Container>
	);
}

export default QueryError;
