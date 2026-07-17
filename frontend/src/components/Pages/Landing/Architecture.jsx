import { Boxes, CloudCog, Code2, Database, GitBranch, Server, Sparkles } from "lucide-react";

function ArchitectureSection() {
	const layers = [
		{
			icon: <Server size={22} />,
			title: "Application Layer",
			items: ["Backend Services", "APIs", "SaaS Applications", "Business Systems"],
		},
		{
			icon: <Code2 size={22} />,
			title: "Ingestion Layer",
			items: ["FastAPI Gateway", "Batch Processing", "Authentication", "Validation"],
		},
		{
			icon: <GitBranch size={22} />,
			title: "Intelligence Pipeline",
			items: ["Parser Registry", "Semantic Events", "Rule Engine", "Correlation"],
			highlight: true,
		},
		{
			icon: <CloudCog size={22} />,
			title: "AI Intelligence",
			items: ["AWS Bedrock", "Incident Analysis", "Recommendations", "Operational Reasoning"],
		},
		{
			icon: <Database size={22} />,
			title: "Persistence Layer",
			items: ["Raw Logs", "Events", "Signals", "Incidents"],
		},
	];

	return (
		<section id="architecture" className="bg-surface relative overflow-hidden py-32">
			{/* Background */}

			<div className="absolute inset-0">
				<div className="bg-accent/5 absolute bottom-0 left-1/2 h-[30rem] w-[30rem] -translate-x-1/2 rounded-full blur-[150px]" />

				<div className="absolute inset-0 bg-[linear-gradient(to_right,var(--color-border)_1px,transparent_1px),linear-gradient(to_bottom,var(--color-border)_1px,transparent_1px)] [background-size:80px_80px] opacity-[0.03]" />
			</div>

			<div className="relative mx-auto max-w-7xl px-6">
				{/* Header */}

				<div className="mx-auto max-w-3xl text-center">
					<div className="border-primary-300 bg-primary-100 text-primary-700 dark:border-primary-500/20 dark:bg-primary-500/10 dark:text-primary-300 inline-flex items-center gap-2 rounded-full border px-4 py-2 text-sm font-semibold">
						<Sparkles size={15} />
						System Architecture
					</div>

					<h2 className="text-t-primary mt-6 font-['Space_Grotesk'] text-4xl font-bold tracking-tight md:text-5xl">
						Built as an intelligence
						<br />
						<span className="text-primary">pipeline, not a log collector.</span>
					</h2>

					<p className="text-t-muted mt-6 text-lg leading-8">
						SignalOps separates ingestion, normalization, detection, correlation, and
						reasoning into independent layers. Each component has a focused
						responsibility and can evolve independently.
					</p>
				</div>

				{/* Architecture Flow */}

				<div className="relative mt-20">
					<div className="bg-border absolute top-0 left-1/2 hidden h-full w-px -translate-x-1/2 lg:block" />

					<div className="space-y-8">
						{layers.map((layer, index) => (
							<div
								key={layer.title}
								className={`relative flex flex-col gap-6 lg:flex-row ${
									index % 2 === 0 ? "lg:flex-row" : "lg:flex-row-reverse"
								}`}
							>
								{/* Connector */}

								<div className="absolute top-12 left-1/2 hidden -translate-x-1/2 lg:block">
									<div
										className={`h-5 w-5 rounded-full border-4 ${
											layer.highlight
												? "border-primary bg-primary"
												: "border-border bg-bg"
										}`}
									/>
								</div>

								{/* Card */}

								<div className="w-full lg:w-1/2">
									<div
										className={`group rounded-3xl border p-8 transition-all duration-500 hover:-translate-y-1 hover:shadow-lg ${
											layer.highlight
												? "border-primary/40 bg-primary-100 dark:bg-primary-500/10"
												: "border-border bg-bg"
										}`}
									>
										<div className="flex items-start justify-between">
											<div
												className={`flex h-14 w-14 items-center justify-center rounded-2xl ${
													layer.highlight
														? "bg-primary text-white"
														: "bg-elevated text-primary"
												}`}
											>
												{layer.icon}
											</div>

											<div className="border-border text-t-muted rounded-full border px-3 py-1 text-xs font-semibold">
												LAYER {index + 1}
											</div>
										</div>

										<h3 className="text-t-primary mt-7 text-2xl font-bold">
											{layer.title}
										</h3>

										<div className="mt-6 grid gap-3 sm:grid-cols-2">
											{layer.items.map((item) => (
												<div
													key={item}
													className="border-border bg-surface flex items-center gap-3 rounded-xl border px-4 py-3"
												>
													<div className="bg-primary h-2 w-2 rounded-full" />

													<span className="text-t-secondary text-sm font-medium">
														{item}
													</span>
												</div>
											))}
										</div>
									</div>
								</div>

								{/* Empty Side */}

								<div className="hidden lg:block lg:w-1/2" />
							</div>
						))}
					</div>
				</div>

				{/* Bottom Architecture Summary */}

				<div className="border-border bg-bg mt-24 rounded-[2rem] border p-10 shadow-md lg:p-14">
					<div className="flex flex-col items-center justify-between gap-10 lg:flex-row">
						<div>
							<div className="flex items-center gap-3">
								<div className="bg-primary-100 text-primary dark:bg-primary-500/10 rounded-xl p-3">
									<Boxes size={22} />
								</div>

								<p className="text-primary font-semibold">Core Design Principle</p>
							</div>

							<h3 className="text-t-primary mt-5 font-['Space_Grotesk'] text-3xl font-bold">
								Every stage creates a more meaningful layer of understanding.
							</h3>

							<p className="text-t-muted mt-5 max-w-3xl text-lg leading-8">
								Raw logs are preserved for auditing and replay, while normalized
								events become the foundation for rules, analytics, correlation, and
								AI reasoning.
							</p>
						</div>

						<div className="border-border bg-surface shrink-0 rounded-3xl border px-8 py-6">
							<div className="flex items-center gap-4 text-sm font-semibold">
								<span className="bg-elevated text-t-primary rounded-xl px-4 py-3">
									Logs
								</span>

								<span className="text-primary">→</span>

								<span className="bg-primary-100 text-primary dark:bg-primary-500/10 rounded-xl px-4 py-3">
									Events
								</span>

								<span className="text-primary">→</span>

								<span className="bg-accent-100 text-accent-700 dark:bg-accent-500/10 rounded-xl px-4 py-3">
									Intelligence
								</span>
							</div>
						</div>
					</div>
				</div>
			</div>
		</section>
	);
}

export default ArchitectureSection;
