import { LoaderCircle, RefreshCw } from "lucide-react";

import Button from "@/components/Button";

function QueryPageHeader({
	title,
	description,
	actions,
	onRefresh,
	isRefreshing = false,
	isPaginationPageLoading = false,
	className = "",
}) {
	return (
		<section
			className={`flex flex-col gap-4 md:flex-row md:items-end md:justify-between ${className}`}
		>
			<div>
				<h1 className="text-t-primary font-['Space_Grotesk'] text-3xl font-bold tracking-tight">
					{title}
				</h1>
				{description && (
					<p className="text-t-muted mt-2 max-w-2xl text-sm leading-6">{description}</p>
				)}
			</div>

			<div className="flex items-center gap-3">
				{isPaginationPageLoading && (
					<div className="text-t-muted flex items-center gap-2 text-sm">
						<LoaderCircle size={16} className="animate-spin" />
					</div>
				)}

				{onRefresh && (
					<Button
						variant="secondary"
						leftIcon={
							<RefreshCw size={16} className={isRefreshing ? "animate-spin" : ""} />
						}
						onClick={onRefresh}
						disabled={isRefreshing}
					>
						Refresh
					</Button>
				)}

				{actions}
			</div>
		</section>
	);
}

export default QueryPageHeader;
