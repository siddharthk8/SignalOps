import { Bot, Braces, Gauge, Layers3, Network, ShieldCheck, Sparkles } from "lucide-react";

function FeaturesSection() {
	const features = [
		{
			icon: <Braces size={24} />,
			title: "Semantic Normalization",
			description:
				"Different application logs with different formats are transformed into a unified event model that the entire platform understands.",
			tag: "Core Engine",
		},
		{
			icon: <Layers3 size={24} />,
			title: "Hybrid Parsing Architecture",
			description:
				"Deterministic parsers handle known patterns first while AI intelligently handles unknown and ambiguous application logs.",
			tag: "Parser Registry",
		},
		{
			icon: <Gauge size={24} />,
			title: "Rule-Based Intelligence",
			description:
				"Operational rules continuously evaluate semantic events and convert meaningful patterns into actionable signals.",
			tag: "Detection",
		},
		{
			icon: <Network size={24} />,
			title: "Incident Correlation",
			description:
				"Individual signals become complete incidents by understanding users, entities, sessions, and time relationships.",
			tag: "Correlation",
		},
		{
			icon: <Bot size={24} />,
			title: "AI Operational Reasoning",
			description:
				"Amazon Bedrock analyzes correlated incidents and generates summaries, probable causes, and recommendations.",
			tag: "Artificial Intelligence",
		},
		{
			icon: <ShieldCheck size={24} />,
			title: "Application-Focused Observability",
			description:
				"Built specifically for backend services, APIs, SaaS platforms, and business applications—not infrastructure noise.",
			tag: "Architecture",
		},
	];

	return (
		<section id="features" className="relative overflow-hidden bg-bg py-32">
			{/* Background */}
			<div className="absolute inset-0">
				<div className="absolute right-0 top-1/3 h-[32rem] w-[32rem] rounded-full bg-accent/5 blur-[140px]" />

				<div className="absolute inset-0 bg-[radial-gradient(var(--color-border)_1px,transparent_1px)] [background-size:28px_28px] opacity-[0.04]" />
			</div>

			<div className="relative mx-auto max-w-7xl px-6">
				{/* Header */}

				<div className="flex flex-col justify-between gap-8 lg:flex-row lg:items-end">
					<div className="max-w-3xl">
						<div className="inline-flex items-center gap-2 rounded-full border border-primary-300 bg-primary-100 px-4 py-2 text-sm font-semibold text-primary-700 dark:border-primary-500/20 dark:bg-primary-500/10 dark:text-primary-300">
							<Sparkles size={15} />
							Platform Capabilities
						</div>

						<h2 className="mt-6 font-['Space_Grotesk'] text-4xl font-bold tracking-tight text-t-primary md:text-5xl">
							Everything needed to turn
							<br />
							<span className="text-primary">logs into intelligence.</span>
						</h2>

						<p className="mt-6 text-lg leading-8 text-t-muted">
							SignalOps combines deterministic engineering, semantic understanding,
							and AI reasoning into a single operational intelligence pipeline.
						</p>
					</div>
				</div>

				{/* Feature Grid */}

				<div className="mt-20 grid gap-6 md:grid-cols-2 lg:grid-cols-3">
					{features.map((feature, index) => (
						<div
							key={feature.title}
							className="group relative overflow-hidden rounded-3xl border border-border bg-surface p-8 transition-all duration-500 hover:-translate-y-2 hover:border-primary/40 hover:shadow-lg"
						>
							{/* Hover glow */}

							<div className="absolute -right-16 -top-16 h-40 w-40 rounded-full bg-primary/10 opacity-0 blur-3xl transition-opacity duration-500 group-hover:opacity-100" />

							<div className="relative">
								<div className="flex items-center justify-between">
									<div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-primary-100 text-primary transition-all duration-300 group-hover:scale-110 dark:bg-primary-500/10">
										{feature.icon}
									</div>

									<span className="rounded-full border border-border px-3 py-1 text-xs font-medium text-t-muted">
										{feature.tag}
									</span>
								</div>

								<h3 className="mt-8 text-xl font-bold text-t-primary">
									{feature.title}
								</h3>

								<p className="mt-4 leading-7 text-t-muted">{feature.description}</p>

								<div className="mt-8 flex items-center gap-2 text-sm font-semibold text-primary opacity-0 transition-all duration-300 group-hover:translate-x-1 group-hover:opacity-100">
									Learn more
									<span>→</span>
								</div>
							</div>

							{/* Index indicator */}

							<div className="absolute bottom-6 right-8 text-5xl font-bold text-border/40">
								0{index + 1}
							</div>
						</div>
					))}
				</div>

				{/* Highlight Banner */}

				<div className="mt-20 rounded-[2rem] border border-border bg-surface p-10 shadow-md lg:p-14">
					<div className="grid gap-10 lg:grid-cols-[1fr_auto] lg:items-center">
						<div>
							<div className="flex items-center gap-3">
								<div className="rounded-xl bg-accent-100 p-3 text-accent-700 dark:bg-accent-500/10 dark:text-accent">
									<Bot size={22} />
								</div>

								<p className="font-semibold text-accent">
									AI is an accelerator, not the foundation
								</p>
							</div>

							<h3 className="mt-6 font-['Space_Grotesk'] text-3xl font-bold text-t-primary">
								Deterministic systems first.
								<br />
								AI intelligence where it matters.
							</h3>

							<p className="mt-5 max-w-3xl text-lg leading-8 text-t-muted">
								SignalOps avoids treating AI as a black-box parser. Reliable rules
								handle predictable scenarios while AI provides semantic
								understanding for unknown events and operational reasoning.
							</p>
						</div>

						<div className="flex justify-center">
							<div className="rounded-3xl border border-primary/20 bg-primary-100 px-8 py-10 text-center dark:bg-primary-500/10">
								<div className="text-5xl font-bold text-primary">2</div>

								<p className="mt-2 text-sm font-semibold uppercase tracking-widest text-t-muted">
									Processing Layers
								</p>

								<div className="mt-6 space-y-2 text-sm">
									<div className="rounded-xl bg-surface px-5 py-3 font-semibold text-t-primary">
										Rule Engine
									</div>

									<div className="text-t-muted">↓</div>

									<div className="rounded-xl bg-surface px-5 py-3 font-semibold text-t-primary">
										AI Reasoning
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</section>
	);
}

export default FeaturesSection;
