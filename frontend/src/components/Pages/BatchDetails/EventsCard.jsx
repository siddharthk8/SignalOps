import { CalendarClock, CheckCircle2, Sparkles } from "lucide-react";

import Collapsible from "@/components/Collapsible";
import ExpandableList from "@/components/ExpandableList";

const severityClasses = {
	low: "bg-success/10 text-success",
	medium: "bg-warning/10 text-warning",
	high: "bg-error/10 text-error",
	critical: "bg-error text-white",
};

const parsingMethodClasses = {
	regex: "bg-primary/10 text-primary",
	heuristic: "bg-accent/10 text-accent",
	ai: "bg-info/10 text-info",
};
function EventRow({ event }) {
	return (
		<Collapsible
			className="hover:bg-muted/20 border-border border-t transition-colors"
			header={
				<div className="min-w-0 flex-1">
					<div className="mb-3 flex flex-wrap items-center gap-2">
						<div className="bg-primary/10 text-primary flex h-8 w-8 items-center justify-center rounded-md">
							<CheckCircle2 size={15} />
						</div>

						<span className="font-semibold">
							{event.event_type.replaceAll("_", " ").toUpperCase()}
						</span>

						<span
							className={`rounded-md px-2 py-0.5 text-[11px] font-medium ${
								severityClasses[event.severity]
							}`}
						>
							{event.severity.toUpperCase()}
						</span>

						<span className="bg-muted text-t-muted rounded-md px-2 py-0.5 text-[11px] font-medium">
							{Math.round(event.confidence * 100)}%
						</span>
					</div>

					<div className="text-t-muted flex flex-wrap items-center gap-4 text-sm">
						{event.timestamp && (
							<div className="flex items-center gap-1.5">
								<CalendarClock size={14} />
								{new Date(event.timestamp).toLocaleString()}
							</div>
						)}

						{event.entity_id && <div>Entity #{event.entity_id}</div>}
					</div>
				</div>
			}
		>
			<div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
				<div>
					<p className="text-t-muted text-[11px] tracking-wide uppercase">Event Type</p>

					<p className="mt-1 text-sm font-medium">{event.event_type}</p>
				</div>

				<div>
					<p className="text-t-muted text-[11px] tracking-wide uppercase">Severity</p>

					<span
						className={`mt-1 inline-flex rounded-md px-2 py-1 text-xs font-medium ${
							severityClasses[event.severity]
						}`}
					>
						{event.severity}
					</span>
				</div>

				<div>
					<p className="text-t-muted text-[11px] tracking-wide uppercase">Confidence</p>

					<p className="mt-1 text-sm font-medium">
						{Math.round(event.confidence * 100)}%
					</p>
				</div>

				<div>
					<p className="text-t-muted text-[11px] tracking-wide uppercase">
						Parsing Method
					</p>

					<span
						className={`mt-1 inline-flex rounded-md px-2 py-1 text-xs font-medium ${
							parsingMethodClasses[event.parsing_method]
						}`}
					>
						{event.parsing_method}
					</span>
				</div>

				<div>
					<p className="text-t-muted text-[11px] tracking-wide uppercase">Log ID</p>

					<p className="mt-1 text-sm font-medium">#{event.log_id}</p>
				</div>

				<div>
					<p className="text-t-muted text-[11px] tracking-wide uppercase">Entity ID</p>

					<p className="mt-1 text-sm font-medium">
						{event.entity_id ? `#${event.entity_id}` : "—"}
					</p>
				</div>

				{event.timestamp && (
					<div className="sm:col-span-2 lg:col-span-3">
						<p className="text-t-muted text-[11px] tracking-wide uppercase">
							Timestamp
						</p>

						<p className="mt-1 text-sm font-medium">
							{new Date(event.timestamp).toLocaleString()}
						</p>
					</div>
				)}
			</div>
		</Collapsible>
	);
}

function EventsCard({ events }) {
	return (
		<section className="bg-surface border-border overflow-hidden rounded-md border">
			<div className="border-border flex items-center justify-between border-b px-5 py-4">
				<div>
					<h2 className="text-base font-semibold">Semantic Events</h2>

					<p className="text-t-muted mt-1 text-sm">
						Normalized events inferred from the raw application logs.
					</p>
				</div>

				<div className="bg-primary/10 text-primary flex h-9 w-9 items-center justify-center rounded-md">
					<Sparkles size={18} />
				</div>
			</div>

			{events.length === 0 ? (
				<div className="px-5 py-12 text-center">
					<Sparkles size={28} className="text-t-muted mx-auto mb-3" />

					<h3 className="font-medium">No Events Generated</h3>

					<p className="text-t-muted mt-2 text-sm">
						No semantic events were produced for this batch.
					</p>
				</div>
			) : (
				<ExpandableList
					items={events}
					limit={5}
					className="divide-border divide-y"
					renderItem={(event) => <EventRow key={event.id} event={event} />}
				/>
			)}
		</section>
	);
}

export default EventsCard;
