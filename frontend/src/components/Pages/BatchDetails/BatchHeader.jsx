import { ArrowLeft, CalendarDays, Clock3, Database } from "lucide-react";
import { Link } from "react-router";

function BatchHeader({ batchId, createdAt }) {
	const created = new Date(createdAt);

	return (
		<header className="border-border border-b pb-8">
			<Link
				to={-1}
				className="text-t-muted hover:text-foreground mb-6 inline-flex items-center gap-2 text-sm font-medium transition-colors"
			>
				<ArrowLeft size={15} />
				Back
			</Link>

			<div className="flex flex-col gap-8 lg:flex-row lg:items-end lg:justify-between">
				{/* Left */}
				<div className="flex items-start gap-4">
					<div className="bg-primary/10 border-primary/20 flex h-14 w-14 shrink-0 items-center justify-center rounded-md border">
						<Database className="text-primary" size={24} />
					</div>

					<div>
						<div className="mb-2 flex items-center gap-3">
							<span className="text-t-muted text-[11px] font-semibold tracking-[0.18em] uppercase">
								Batch
							</span>

							<span className="bg-success/10 text-success border-success/20 rounded-md border px-2 py-1 text-[11px] font-medium">
								Processed
							</span>
						</div>

						{/* <h1 className="font-['Space_Grotesk'] text-4xl font-semibold tracking-tight">
							#{batchId}
						</h1> */}

						<p className="text-t-muted mt-3 max-w-2xl text-sm leading-6">
							Semantic intelligence, extracted entities, AI analyses, and security
							findings produced from this ingestion batch.
						</p>
					</div>
				</div>

				{/* Right */}
				<div className="flex gap-10 lg:gap-14">
					<div>
						<div className="text-t-muted mb-2 flex items-center gap-2 text-[11px] font-medium tracking-[0.18em] uppercase">
							<CalendarDays size={14} />
							Created
						</div>

						<div className="text-base font-semibold">
							{created.toLocaleDateString(undefined, {
								weekday: "short",
								month: "short",
								day: "numeric",
								year: "numeric",
							})}
						</div>
					</div>

					<div>
						<div className="text-t-muted mb-2 flex items-center gap-2 text-[11px] font-medium tracking-[0.18em] uppercase">
							<Clock3 size={14} />
							Time
						</div>

						<div className="text-base font-semibold">
							{created.toLocaleTimeString([], {
								hour: "2-digit",
								minute: "2-digit",
							})}
						</div>
					</div>
				</div>
			</div>
		</header>
	);
}

export default BatchHeader;
