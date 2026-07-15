import {
	Activity,
	AlertTriangle,
	ArrowDown,
	ArrowRight,
	BrainCircuit,
	CheckCircle2,
	Clock3,
	Database,
	FileInput,
	FileText,
	Network,
	Search,
	Sparkles,
	Zap,
} from "lucide-react";

function WorkflowSection() {
	const steps = [
		{
			icon: <FileInput size={22} />,
			title: "Log Ingestion",
			description: "Applications send batches of logs through the FastAPI ingestion layer.",
			meta: "POST /api/v1/logs",
		},
		{
			icon: <Database size={22} />,
			title: "Persistence",
			description: "Raw logs are stored for replay, auditing, and debugging purposes.",
			meta: "Raw Events",
		},
		{
			icon: <Zap size={22} />,
			title: "Normalization",
			description: "Parser registry converts application logs into semantic events.",
			meta: "Event Intelligence",
		},
		{
			icon: <Activity size={22} />,
			title: "Detection",
			description: "Rules evaluate events and create operational signals.",
			meta: "Signal Generation",
		},
		{
			icon: <Network size={22} />,
			title: "Correlation",
			description: "Related signals are grouped into meaningful incidents.",
			meta: "Incident Engine",
		},
		{
			icon: <Sparkles size={22} />,
			title: "AI Analysis",
			description: "Bedrock generates summaries, causes, and recommendations.",
			meta: "AI Reasoning",
		},
	];

	return (
		<section id="workflow" className="relative overflow-hidden bg-bg py-32">
			{/* Background */}

			<div className="absolute inset-0">
				<div className="absolute left-1/2 top-0 h-[34rem] w-[34rem] -translate-x-1/2 rounded-full bg-accent/5 blur-[160px]" />
			</div>

			<div className="relative mx-auto max-w-7xl px-6">
				{/* Header */}

				<div className="mx-auto max-w-3xl text-center">
					<div className="inline-flex items-center gap-2 rounded-full border border-primary-300 bg-primary-100 px-4 py-2 text-sm font-semibold text-primary-700 dark:border-primary-500/20 dark:bg-primary-500/10 dark:text-primary-300">
						<Sparkles size={15} />
						End-to-End Pipeline
					</div>

					<h2 className="mt-6 font-['Space_Grotesk'] text-4xl font-bold tracking-tight text-t-primary md:text-5xl">
						From ingestion to
						<br />
						<span className="text-primary">operational decisions.</span>
					</h2>

					<p className="mt-6 text-lg leading-8 text-t-muted">
						Every request moves through a carefully designed intelligence pipeline. Each
						stage adds context until raw application output becomes a meaningful
						operational decision.
					</p>
				</div>

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

				{/* Workflow Timeline */}

				<div className="relative mt-20">
					<div className="absolute left-8 top-0 hidden h-full w-px bg-border md:block" />

					<div className="space-y-8">
						{steps.map((step, index) => (
							<div key={step.title} className="relative flex gap-8">
								{/* Number */}

								<div className="relative z-10 hidden md:flex">
									<div className="flex h-16 w-16 items-center justify-center rounded-2xl border border-border bg-surface text-primary shadow-md">
										{step.icon}
									</div>
								</div>

								{/* Card */}

								<div className="flex-1 rounded-3xl border border-border bg-surface p-8 transition-all duration-300 hover:-translate-y-1 hover:border-primary/40 hover:shadow-lg">
									<div className="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
										<div className="flex gap-5">
											<div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-primary-100 text-primary md:hidden dark:bg-primary-500/10">
												{step.icon}
											</div>

											<div>
												<div className="flex items-center gap-3">
													<h3 className="text-xl font-bold text-t-primary">
														{step.title}
													</h3>

													<span className="rounded-full border border-border px-3 py-1 text-xs font-semibold text-t-muted">
														0{index + 1}
													</span>
												</div>

												<p className="mt-3 max-w-2xl leading-7 text-t-muted">
													{step.description}
												</p>
											</div>
										</div>

										<div className="flex items-center gap-3 rounded-xl bg-elevated px-4 py-3 text-sm font-semibold text-t-secondary">
											<Clock3 size={16} />

											{step.meta}
										</div>
									</div>
								</div>
							</div>
						))}
					</div>
				</div>

				{/* Final Flow Card */}

				<div className="mt-20 rounded-[2rem] border border-primary/20 bg-primary-100 p-10 dark:bg-primary-500/10 lg:p-14">
					<div className="flex flex-col items-center justify-between gap-10 lg:flex-row">
						<div>
							<div className="flex items-center gap-3">
								<div className="rounded-xl bg-primary p-3 text-white">
									<CheckCircle2 size={22} />
								</div>

								<span className="font-semibold text-primary">
									Complete Intelligence Cycle
								</span>
							</div>

							<h3 className="mt-6 font-['Space_Grotesk'] text-3xl font-bold text-t-primary">
								Every layer contributes to the final operational understanding.
							</h3>

							<p className="mt-4 max-w-2xl text-lg leading-8 text-t-muted">
								The platform preserves raw evidence while building increasingly
								intelligent representations of system behavior.
							</p>
						</div>

						<div className="flex flex-wrap items-center justify-center gap-3">
							{["Logs", "Events", "Signals", "Incidents", "AI"].map((item, index) => (
								<div key={item} className="flex items-center gap-3">
									<div className="rounded-xl border border-border bg-surface px-5 py-3 text-sm font-bold text-t-primary">
										{item}
									</div>

									{index !== 4 && (
										<ArrowRight size={18} className="text-primary" />
									)}
								</div>
							))}
						</div>
					</div>
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

export default WorkflowSection;
