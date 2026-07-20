import { useMutation, useQueryClient } from "@tanstack/react-query";
import { AlertTriangle, CalendarClock, CheckCircle2, ShieldAlert } from "lucide-react";

import { markIncidentResolved } from "@/api";
import Button from "@/components/Button";
import authenticatedClient from "@/core/api/customClient";

const severityClasses = {
	low: "bg-success/10 text-success",
	medium: "bg-warning/10 text-warning",
	high: "bg-error/10 text-error",
	critical: "bg-error text-white",
};

const statusClasses = {
	open: "bg-warning/10 text-warning",
	resolved: "bg-success/10 text-success",
};

function IncidentsCard({ incidents }) {
	const queryClient = useQueryClient();

	const { mutate, isPending } = useMutation({
		mutationFn: (incidentId) =>
			markIncidentResolved({
				client: authenticatedClient,
				path: {
					incident_id: incidentId,
				},
			}),

		onSuccess: () => {
			queryClient.invalidateQueries({
				queryKey: ["batch"],
			});
		},
	});

	return (
		<section className="bg-surface border-border overflow-hidden rounded-md border">
			<div className="border-border flex items-center justify-between border-b px-5 py-4">
				<div>
					<h2 className="text-base font-semibold">Correlated Incidents</h2>

					<p className="text-t-muted mt-1 text-sm">
						Operational incidents produced by correlating related signals.
					</p>
				</div>

				<div className="bg-error/10 text-error flex h-9 w-9 items-center justify-center rounded-md">
					<ShieldAlert size={18} />
				</div>
			</div>

			{incidents.length === 0 ? (
				<div className="px-5 py-12 text-center">
					<ShieldAlert size={28} className="text-t-muted mx-auto mb-3" />

					<h3 className="font-medium">No Incidents Created</h3>

					<p className="text-t-muted mt-2 text-sm">
						No correlated operational incidents were generated.
					</p>
				</div>
			) : (
				<div className="divide-border divide-y">
					{incidents.map((incident) => (
						<div
							key={incident.id}
							className="hover:bg-muted/20 px-5 py-5 transition-colors"
						>
							<div className="flex flex-col gap-5 lg:flex-row lg:justify-between">
								<div className="min-w-0 flex-1">
									<div className="mb-3 flex flex-wrap items-center gap-2">
										<h3 className="text-lg font-semibold">{incident.title}</h3>

										<span
											className={`rounded-md px-2 py-0.5 text-[11px] font-medium ${
												severityClasses[incident.severity]
											}`}
										>
											{incident.severity.toUpperCase()}
										</span>

										<span
											className={`rounded-md px-2 py-0.5 text-[11px] font-medium ${
												statusClasses[incident.status]
											}`}
										>
											{incident.status.toUpperCase()}
										</span>

										<span className="bg-primary/10 text-primary rounded-md px-2 py-0.5 text-[11px] font-medium">
											{incident.incident_type
												.replaceAll("_", " ")
												.replace(/\b\w/g, (c) => c.toUpperCase())}
										</span>

										<div className="ml-auto">
											{incident.status === "open" ? (
												<Button
													size="sm"
													onClick={() => mutate(incident.id)}
													disabled={isPending}
												>
													{isPending ? "Resolving..." : "Mark Resolved"}
												</Button>
											) : (
												<span className="bg-success/10 text-success rounded-md px-3 py-1 text-xs font-medium">
													Resolved
												</span>
											)}
										</div>
									</div>

									<p className="text-t-muted text-sm leading-6">
										{incident.summary}
									</p>
								</div>

								<div className="border-border min-w-[170px] rounded-md border p-4">
									<div className="text-t-muted text-[11px] tracking-wide uppercase">
										Confidence
									</div>

									<div className="mt-1 text-2xl font-semibold">
										{Math.round(incident.confidence * 100)}%
									</div>

									<div className="bg-muted mt-3 h-2 overflow-hidden rounded-full">
										<div
											className="bg-primary h-full rounded-full"
											style={{
												width: `${incident.confidence * 100}%`,
											}}
										/>
									</div>
								</div>
							</div>

							<div className="border-border mt-5 grid gap-5 border-t pt-5 sm:grid-cols-3">
								<div className="flex items-start gap-3">
									<AlertTriangle size={15} className="text-t-muted mt-0.5" />

									<div>
										<p className="text-t-muted text-[11px] tracking-wide uppercase">
											Incident ID
										</p>

										<p className="text-sm font-medium">#{incident.id}</p>
									</div>
								</div>

								<div className="flex items-start gap-3">
									<CalendarClock size={15} className="text-t-muted mt-0.5" />

									<div>
										<p className="text-t-muted text-[11px] tracking-wide uppercase">
											Detected
										</p>

										<p className="text-sm font-medium">
											{new Date(incident.detected_at).toLocaleString()}
										</p>
									</div>
								</div>

								<div className="flex items-start gap-3">
									<CheckCircle2 size={15} className="text-t-muted mt-0.5" />

									<div>
										<p className="text-t-muted text-[11px] tracking-wide uppercase">
											Last Updated
										</p>

										<p className="text-sm font-medium">
											{new Date(incident.updated_at).toLocaleString()}
										</p>
									</div>
								</div>
							</div>
						</div>
					))}
				</div>
			)}
		</section>
	);
}

export default IncidentsCard;
