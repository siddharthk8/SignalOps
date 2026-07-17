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
		<section id="transformation" className="bg-bg relative overflow-hidden py-32">
			{/* Background */}

			<div className="absolute inset-0">
				<div className="bg-primary/5 absolute top-1/3 left-0 h-[30rem] w-[30rem] rounded-full blur-[140px]" />

				<div className="bg-accent/5 absolute right-0 bottom-0 h-[28rem] w-[28rem] rounded-full blur-[140px]" />
			</div>

			<div className="relative mx-auto max-w-7xl px-6">
				{/* Header */}

				<div className="mx-auto max-w-3xl text-center">
					<div className="border-primary-300 bg-primary-100 text-primary-700 dark:border-primary-500/20 dark:bg-primary-500/10 dark:text-primary-300 inline-flex items-center gap-2 rounded-full border px-4 py-2 text-sm font-semibold">
						<Sparkles size={15} />
						Semantic Transformation
					</div>

					<h2 className="text-t-primary mt-6 font-['Space_Grotesk'] text-4xl font-bold tracking-tight md:text-5xl">
						From noisy logs to
						<br />
						<span className="text-primary">meaningful incidents.</span>
					</h2>

					<p className="text-t-muted mt-6 text-lg leading-8">
						SignalOps does not simply search through text. It understands the
						operational meaning behind application behavior.
					</p>
				</div>

				{/* Transformation */}

				<div className="mt-20 grid gap-8 lg:grid-cols-[1fr_auto_1fr] lg:items-center">
					{/* Raw Logs */}

					<div className="border-border bg-surface rounded-[2rem] border p-8 shadow-md">
						<div className="flex items-center gap-3">
							<div className="bg-error/10 text-error rounded-xl p-3">
								<FileText size={22} />
							</div>

							<div>
								<p className="text-t-muted text-sm font-semibold tracking-wider uppercase">
									Input
								</p>

								<h3 className="text-t-primary text-xl font-bold">
									Raw Application Logs
								</h3>
							</div>
						</div>

						<div className="mt-8 space-y-4 font-mono text-sm">
							<div className="border-border bg-elevated text-t-secondary rounded-xl border p-4">
								<span className="text-error">LOGIN_FAIL</span> user=alex
								ip=192.168.1.12
							</div>

							<div className="border-border bg-elevated text-t-secondary rounded-xl border p-4">
								<span className="text-error">Auth rejected</span> for alex
							</div>

							<div className="border-border bg-elevated text-t-secondary rounded-xl border p-4">
								<span className="text-warning">Password attempt exceeded</span>
							</div>
						</div>

						<div className="text-t-muted mt-8 flex items-center gap-2 text-sm font-semibold">
							<Search size={16} />
							Unstructured application output
						</div>
					</div>

					{/* Arrow */}

					<div className="flex justify-center">
						<div className="border-border bg-surface rounded-full border p-4 shadow-md">
							<ArrowDown size={24} className="text-primary lg:rotate-[-90deg]" />
						</div>
					</div>

					{/* Intelligence */}

					<div className="border-primary/30 bg-primary-100 dark:bg-primary-500/10 rounded-[2rem] border p-8 shadow-lg">
						<div className="flex items-center gap-3">
							<div className="bg-primary rounded-xl p-3 text-white">
								<BrainCircuit size={22} />
							</div>

							<div>
								<p className="text-primary text-sm font-semibold tracking-wider uppercase">
									Output
								</p>

								<h3 className="text-t-primary text-xl font-bold">
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

						<div className="border-primary/20 bg-surface mt-8 rounded-2xl border p-5">
							<div className="text-primary flex items-center gap-2 text-sm font-semibold">
								<AlertTriangle size={16} />
								Generated Incident
							</div>

							<h4 className="text-t-primary mt-3 font-bold">ACCOUNT_TAKEOVER</h4>

							<p className="text-t-muted mt-2 text-sm leading-6">
								Multiple authentication failures followed by successful access
								indicate suspicious account activity.
							</p>

							<div className="text-success mt-4 flex items-center gap-2 text-sm font-semibold">
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
		<div className="border-border bg-surface flex items-center justify-between rounded-xl border px-5 py-4">
			<span className="text-t-muted text-sm">{title}</span>

			<span className="text-t-primary font-semibold">{value}</span>
		</div>
	);
}

function InsightCard({ number, title, description }) {
	return (
		<div className="border-border bg-surface rounded-3xl border p-7 transition-all duration-300 hover:-translate-y-1 hover:shadow-lg">
			<div className="text-border text-4xl font-bold">{number}</div>

			<h3 className="text-t-primary mt-5 text-xl font-bold">{title}</h3>

			<p className="text-t-muted mt-3 leading-7">{description}</p>
		</div>
	);
}

export default TransformationSection;
