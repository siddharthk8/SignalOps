import { BrainCircuit, GitBranchPlus, ShieldCheck, Sparkles } from "lucide-react";

export default function HeroSection() {
	return (
		<section
			id="overview"
			className="border-border bg-bg relative isolate overflow-hidden border-b"
		>
			{/* Background */}
			<div className="absolute inset-0 -z-20">
				<div className="absolute inset-0 bg-[radial-gradient(circle_at_top,rgba(218,138,104,0.10),transparent_45%)] dark:bg-[radial-gradient(circle_at_top,rgba(215,154,130,0.12),transparent_45%)]" />
				<div className="absolute inset-0 bg-[linear-gradient(to_right,var(--color-border)_1px,transparent_1px),linear-gradient(to_bottom,var(--color-border)_1px,transparent_1px)] [background-size:64px_64px] opacity-[0.05]" />
			</div>

			<div className="bg-primary/10 absolute top-0 left-1/2 -z-10 h-[38rem] w-[38rem] -translate-x-1/2 rounded-full blur-[140px]" />

			<div className="mx-auto flex min-h-screen w-full max-w-7xl flex-col justify-center gap-20 px-6 py-28 lg:flex-row lg:items-center lg:justify-between">
				{/* Left */}
				<div className="max-w-3xl">
					<div className="border-primary-300/70 bg-primary-100 text-primary-700 dark:border-primary-500/20 dark:bg-primary-500/10 dark:text-primary-600 inline-flex items-center gap-2 rounded-full border px-4 py-2 text-sm font-semibold">
						<Sparkles size={15} />
						Application Logs Intelligence System
					</div>

					<h1 className="text-t-primary mt-8 font-['Space_Grotesk'] text-5xl leading-[1.05] font-bold tracking-tight md:text-6xl xl:text-7xl">
						Transform
						<br />
						<span className="text-primary">Application Logs</span>
						<br />
						into Operational
						<span className="text-accent"> Intelligence.</span>
					</h1>

					<p className="text-t-muted mt-8 max-w-2xl text-lg leading-8">
						SignalOps converts heterogeneous application logs into semantic events,
						detects meaningful operational signals, correlates related activities into
						incidents, and delivers AI-generated operational analysis powered by Amazon
						Bedrock.
					</p>

					<div className="mt-16 flex flex-wrap gap-8">
						<Stat
							icon={<BrainCircuit size={18} />}
							title="Hybrid Parsing"
							subtitle="Regex + AI"
						/>
						<Stat
							icon={<GitBranchPlus size={18} />}
							title="Incident Correlation"
							subtitle="Signals → Incidents"
						/>
						<Stat
							icon={<ShieldCheck size={18} />}
							title="Bedrock AI"
							subtitle="Operational Reasoning"
						/>
					</div>
				</div>

				{/* Right */}
				<div className="relative flex w-full max-w-xl justify-center">
					<div className="border-border bg-surface/70 relative w-full rounded-2xl border p-8 shadow-lg backdrop-blur">
						<div className="mb-8 flex items-center justify-between">
							<div>
								<p className="text-t-muted text-sm">
									Semantic Intelligence Pipeline
								</p>

								<h3 className="text-t-primary mt-1 text-xl font-bold">
									Live Processing Flow
								</h3>
							</div>

							<div className="flex items-center gap-2">
								<span className="bg-success h-2.5 w-2.5 animate-pulse rounded-full" />
								<span className="text-success text-xs font-medium">ACTIVE</span>
							</div>
						</div>

						<div className="space-y-4">
							<PipelineStep
								title="Raw Application Logs"
								description="Incoming heterogeneous logs"
							/>

							<Connector />
							<PipelineStep
								title="Semantic Events"
								description="Normalized event inference"
								active
							/>

							<Connector />
							<PipelineStep
								title="Signals"
								description="Rule-based anomaly detection"
							/>

							<Connector />
							<PipelineStep
								title="Incidents"
								description="Context-aware correlation"
							/>

							<Connector />
							<PipelineStep
								title="AI Analysis"
								description="Bedrock operational reasoning"
							/>
						</div>
					</div>

					{/* Floating Raw Log */}
					<div className="border-border bg-surface absolute top-15 -left-10 hidden w-52 rounded-xl border p-4 shadow-md backdrop-blur lg:block">
						<div className="text-t-muted text-xs font-semibold tracking-wider uppercase">
							Incoming Log
						</div>

						<div className="bg-elevated text-warning mt-3 rounded-lg p-3 font-mono text-sm">
							LOGIN_FAIL
							<br />
							user=alex
						</div>
					</div>

					{/* Floating Incident */}
					<div className="border-border bg-surface absolute -right-10 -bottom-6 hidden w-60 rounded-xl border p-4 shadow-md backdrop-blur lg:block">
						<div className="text-t-muted text-xs font-semibold tracking-wider uppercase">
							Generated Incident
						</div>

						<div className="mt-3">
							<div className="text-primary font-semibold">ACCOUNT_TAKEOVER</div>

							<p className="text-t-muted mt-2 text-sm leading-6">
								Multiple authentication failures followed by a successful login
								indicate suspicious account activity.
							</p>
						</div>
					</div>
				</div>
			</div>
		</section>
	);
}

function PipelineStep({ title, description, active = false }) {
	return (
		<div
			className={`rounded-2xl border p-5 transition-all duration-300 ${
				active
					? "border-primary/40 bg-primary-100 dark:bg-primary-500/10"
					: "border-border bg-elevated hover:border-primary/30"
			}`}
		>
			<div className="flex items-center justify-between">
				<div>
					<h4 className="text-t-primary font-semibold">{title}</h4>
					<p className="text-t-muted mt-1 text-sm">{description}</p>
				</div>

				<div className={`h-3 w-3 rounded-full ${active ? "bg-primary" : "bg-border"}`} />
			</div>
		</div>
	);
}

function Connector() {
	return (
		<div className="flex justify-center">
			<div className="bg-border h-6 w-px" />
		</div>
	);
}

function Stat({ icon, title, subtitle }) {
	return (
		<div className="flex items-center gap-4">
			<div className="bg-primary-100 text-primary dark:bg-primary-500/10 rounded-xl p-3">
				{icon}
			</div>

			<div>
				<div className="text-t-primary font-semibold">{title}</div>
				<div className="text-t-muted text-sm">{subtitle}</div>
			</div>
		</div>
	);
}
