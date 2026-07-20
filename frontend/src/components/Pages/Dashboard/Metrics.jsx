import { AlertTriangle, Database, ShieldAlert } from "lucide-react";

function DashboardMetrics({ data }) {
	const metrics = [
		{
			title: "Source Applications",
			value: data.source_apps_count,
			icon: Database,
			color: "text-primary",
			bg: "bg-primary/10",
			accent: "bg-primary",
		},
		{
			title: "Total Incidents",
			value: data.incidents_count,
			icon: AlertTriangle,
			color: "text-warning",
			bg: "bg-warning/10",
			accent: "bg-warning",
		},
		{
			title: "Unresolved Incidents",
			value: data.unresolved_incidents_count,
			icon: ShieldAlert,
			color: "text-error",
			bg: "bg-error/10",
			accent: "bg-error",
		},
	];

	return (
		<section className="grid gap-5 sm:grid-cols-2 xl:grid-cols-3">
			{metrics.map((metric) => {
				const Icon = metric.icon;

				return (
					<div
						key={metric.title}
						className="border-border bg-surface group hover:border-primary/20 overflow-hidden rounded-lg border transition-all duration-200 hover:shadow-sm"
					>
						<div className={`h-0.5 ${metric.accent}`} />

						<div className="p-5">
							<div className="flex items-start justify-between">
								<div>
									<p className="text-t-muted text-sm font-medium">
										{metric.title}
									</p>

									<h2 className="text-t-primary mt-2 text-3xl font-bold tracking-tight">
										{metric.value.toLocaleString()}
									</h2>
								</div>

								<div
									className={`flex size-11 items-center justify-center rounded-md ${metric.bg}`}
								>
									<Icon size={20} className={metric.color} strokeWidth={2} />
								</div>
							</div>
						</div>
					</div>
				);
			})}
		</section>
	);
}

export default DashboardMetrics;
