import { AlertTriangle, RefreshCcw } from "lucide-react";

import Button from "@/components/Button";
import Container from "@/components/Container";

function QueryError({
	title = "Unable to load data",
	message = "Something went wrong while fetching the requested information.",
	onRetry,
}) {
	return (
		<Container>
			<div className="flex min-h-[60vh] items-center justify-center py-12">
				<div className="w-full max-w-md">
					<div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full border border-red-500/15 bg-red-500/8">
						<AlertTriangle size={26} className="text-red-500" strokeWidth={2} />
					</div>

					<div className="mt-7 text-center">
						<h2 className="text-t-primary text-2xl font-semibold tracking-tight">
							{title}
						</h2>

						<p className="text-t-muted mx-auto mt-3 max-w-sm leading-7">{message}</p>
					</div>

					{onRetry && (
						<div className="mt-8 flex justify-center">
							<Button onClick={onRetry} leftIcon={<RefreshCcw size={16} />}>
								Try Again
							</Button>
						</div>
					)}

					<div className="border-border mt-10 border-t pt-3 text-center">
						<p className="text-t-muted text-xs">
							If the problem persists, please refresh the page or try again later.
						</p>
					</div>
				</div>
			</div>
		</Container>
	);
}

export default QueryError;
