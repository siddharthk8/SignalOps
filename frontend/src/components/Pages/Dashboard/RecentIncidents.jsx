import { AlertTriangle } from "lucide-react";

function getSeverityStyles(severity) {
	switch (severity) {
		case "critical":
			return {
				dot: "bg-error",
				badge: "bg-error/10 text-error",
			};
		case "high":
			return {
				dot: "bg-warning",
				badge: "bg-warning/10 text-warning",
			};
		case "medium":
			return {
				dot: "bg-primary",
				badge: "bg-primary/10 text-primary",
			};
		default:
			return {
				dot: "bg-success",
				badge: "bg-success/10 text-success",
			};
	}
}

function getStatusStyles(status) {
	switch (status) {
		case "resolved":
			return "bg-success/10 text-success";

		default:
			return "bg-error/10 text-error";
	}
}

function formatType(type) {
	return type
		.split("_")
		.map((word) => word[0].toUpperCase() + word.slice(1))
		.join(" ");
}

function formatTime(date) {
	return new Intl.DateTimeFormat("en-US", {
		month: "short",
		day: "numeric",
		hour: "numeric",
		minute: "2-digit",
	}).format(new Date(date));
}

function RecentIncidents({ incidents }) {
	return (
		<section className="border-border bg-surface flex h-full flex-col overflow-hidden rounded-lg border">
			<div className="border-border flex items-center justify-between border-b px-6 py-5">
				<div>
					<h2 className="text-t-primary text-lg font-semibold">Recent Incidents</h2>

					<p className="text-t-muted mt-1 text-sm">
						Last {incidents.length} detected incidents.
					</p>
				</div>

				<div className="bg-warning/10 text-warning flex size-10 items-center justify-center rounded-md">
					<AlertTriangle size={18} />
				</div>
			</div>

			{incidents.length === 0 ? (
				<div className="text-t-muted flex flex-1 items-center justify-center py-12 text-sm">
					No recent incidents.
				</div>
			) : (
				<div className="divide-border divide-y">
					{incidents.map((incident) => {
						const severity = getSeverityStyles(incident.severity);

						return (
							<div
								key={incident.id}
								className="hover:bg-bg/40 flex items-start gap-4 px-6 py-4 transition-colors"
							>
								<div className={`mt-2 size-2 rounded-full ${severity.dot}`} />

								<div className="min-w-0 flex-1">
									<div className="flex items-start justify-between gap-3">
										<h3 className="text-t-primary truncate text-sm font-semibold">
											{incident.title}
										</h3>

										<span className="text-t-muted shrink-0 text-xs">
											{formatTime(incident.detected_at)}
										</span>
									</div>

									<div className="mt-2 flex flex-wrap items-center gap-2">
										<span className="bg-bg text-t-muted rounded-md px-2 py-1 text-xs">
											{formatType(incident.incident_type)}
										</span>

										<span
											className={`rounded-md px-2 py-1 text-xs font-medium capitalize ${severity.badge}`}
										>
											{incident.severity}
										</span>

										<span
											className={`rounded-md px-2 py-1 text-xs font-medium capitalize ${getStatusStyles(
												incident.status,
											)}`}
										>
											{incident.status}
										</span>
									</div>
								</div>
							</div>
						);
					})}
				</div>
			)}
		</section>
	);
}

export default RecentIncidents;
