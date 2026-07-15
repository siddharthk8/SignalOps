import {
	AlertTriangle,
	ArrowDown,
	BrainCircuit,
	CheckCircle2,
	FileText,
	Search,
	Sparkles,
} from "lucide-react";

function TransformationSection() {
	return (
		<section id="transformation" className="relative overflow-hidden bg-bg py-32">
			{/* Background */}

			<div className="absolute inset-0">
				<div className="absolute left-0 top-1/3 h-[30rem] w-[30rem] rounded-full bg-primary/5 blur-[140px]" />

				<div className="absolute right-0 bottom-0 h-[28rem] w-[28rem] rounded-full bg-accent/5 blur-[140px]" />
			</div>

			<div className="relative mx-auto max-w-7xl px-6">
				{/* Header */}

				<div className="mx-auto max-w-3xl text-center">
					<div className="inline-flex items-center gap-2 rounded-full border border-primary-300 bg-primary-100 px-4 py-2 text-sm font-semibold text-primary-700 dark:border-primary-500/20 dark:bg-primary-500/10 dark:text-primary-300">
						<Sparkles size={15} />
						Semantic Transformation
					</div>

					<h2 className="mt-6 font-['Space_Grotesk'] text-4xl font-bold tracking-tight text-t-primary md:text-5xl">
						From noisy logs to
						<br />
						<span className="text-primary">meaningful incidents.</span>
					</h2>

					<p className="mt-6 text-lg leading-8 text-t-muted">
						SignalOps does not simply search through text. It understands the
						operational meaning behind application behavior.
					</p>
				</div>

				{/* Transformation */}

				<div className="mt-20 grid gap-8 lg:grid-cols-[1fr_auto_1fr] lg:items-center">
					{/* Raw Logs */}

					<div className="rounded-[2rem] border border-border bg-surface p-8 shadow-md">
						<div className="flex items-center gap-3">
							<div className="rounded-xl bg-error/10 p-3 text-error">
								<FileText size={22} />
							</div>

							<div>
								<p className="text-sm font-semibold uppercase tracking-wider text-t-muted">
									Input
								</p>

								<h3 className="text-xl font-bold text-t-primary">
									Raw Application Logs
								</h3>
							</div>
						</div>

						<div className="mt-8 space-y-4 font-mono text-sm">
							<div className="rounded-xl border border-border bg-elevated p-4 text-t-secondary">
								<span className="text-error">LOGIN_FAIL</span> user=alex
								ip=192.168.1.12
							</div>

							<div className="rounded-xl border border-border bg-elevated p-4 text-t-secondary">
								<span className="text-error">Auth rejected</span> for alex
							</div>

							<div className="rounded-xl border border-border bg-elevated p-4 text-t-secondary">
								<span className="text-warning">Password attempt exceeded</span>
							</div>
						</div>

						<div className="mt-8 flex items-center gap-2 text-sm font-semibold text-t-muted">
							<Search size={16} />
							Unstructured application output
						</div>
					</div>

					{/* Arrow */}

					<div className="flex justify-center">
						<div className="rounded-full border border-border bg-surface p-4 shadow-md">
							<ArrowDown size={24} className="text-primary lg:rotate-[-90deg]" />
						</div>
					</div>

					{/* Intelligence */}

					<div className="rounded-[2rem] border border-primary/30 bg-primary-100 p-8 shadow-lg dark:bg-primary-500/10">
						<div className="flex items-center gap-3">
							<div className="rounded-xl bg-primary p-3 text-white">
								<BrainCircuit size={22} />
							</div>

							<div>
								<p className="text-sm font-semibold uppercase tracking-wider text-primary">
									Output
								</p>

								<h3 className="text-xl font-bold text-t-primary">
									Semantic Intelligence
								</h3>
							</div>
						</div>

						<div className="mt-8 space-y-5">
							<EventCard title="Event Type" value="LOGIN_FAIL" />

							<EventCard title="Severity" value="HIGH" />

							<EventCard title="Entity" value="user: alex" />

							<EventCard title="Confidence" value="0.97" />
						</div>

						<div className="mt-8 rounded-2xl border border-primary/20 bg-surface p-5">
							<div className="flex items-center gap-2 text-sm font-semibold text-primary">
								<AlertTriangle size={16} />
								Generated Incident
							</div>

							<h4 className="mt-3 font-bold text-t-primary">ACCOUNT_TAKEOVER</h4>

							<p className="mt-2 text-sm leading-6 text-t-muted">
								Multiple authentication failures followed by successful access
								indicate suspicious account activity.
							</p>

							<div className="mt-4 flex items-center gap-2 text-sm font-semibold text-success">
								<CheckCircle2 size={16} />
								AI analysis completed
							</div>
						</div>
					</div>
				</div>

				{/* Bottom Explanation */}

				<div className="mt-20 grid gap-6 md:grid-cols-3">
					<InsightCard
						number="01"
						title="Normalize"
						description="Convert different log formats into consistent semantic events."
					/>

					<InsightCard
						number="02"
						title="Correlate"
						description="Connect related signals using context, entities, and time windows."
					/>

					<InsightCard
						number="03"
						title="Reason"
						description="Generate operational understanding with AI-powered analysis."
					/>
				</div>
			</div>
		</section>
	);
}

function EventCard({ title, value }) {
	return (
		<div className="flex items-center justify-between rounded-xl border border-border bg-surface px-5 py-4">
			<span className="text-sm text-t-muted">{title}</span>

			<span className="font-semibold text-t-primary">{value}</span>
		</div>
	);
}

function InsightCard({ number, title, description }) {
	return (
		<div className="rounded-3xl border border-border bg-surface p-7 transition-all duration-300 hover:-translate-y-1 hover:shadow-lg">
			<div className="text-4xl font-bold text-border">{number}</div>

			<h3 className="mt-5 text-xl font-bold text-t-primary">{title}</h3>

			<p className="mt-3 leading-7 text-t-muted">{description}</p>
		</div>
	);
}

export default TransformationSection;
