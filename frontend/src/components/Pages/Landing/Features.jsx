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
		<section id="features" className="bg-bg relative overflow-hidden py-32">
			{/* Background */}
			<div className="absolute inset-0">
				<div className="bg-accent/5 absolute top-1/3 right-0 h-[32rem] w-[32rem] rounded-full blur-[140px]" />

				<div className="absolute inset-0 bg-[radial-gradient(var(--color-border)_1px,transparent_1px)] [background-size:28px_28px] opacity-[0.04]" />
			</div>

			<div className="relative mx-auto max-w-7xl px-6">
				{/* Header */}

				<div className="flex flex-col justify-between gap-8 lg:flex-row lg:items-end">
					<div className="max-w-3xl">
						<div className="border-primary-300 bg-primary-100 text-primary-700 dark:border-primary-500/20 dark:bg-primary-500/10 dark:text-primary-600 inline-flex items-center gap-2 rounded-full border px-4 py-2 text-sm font-semibold">
							<Sparkles size={15} />
							Platform Capabilities
						</div>

						<h2 className="text-t-primary mt-6 font-['Space_Grotesk'] text-4xl font-bold tracking-tight md:text-5xl">
							Everything needed to turn
							<br />
							<span className="text-primary">logs into intelligence.</span>
						</h2>

						<p className="text-t-muted mt-6 text-lg leading-8">
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
							className="group border-border bg-surface hover:border-primary/40 relative overflow-hidden rounded-2xl border p-8 transition-all duration-500 hover:-translate-y-2 hover:shadow-lg"
						>
							{/* Hover glow */}

							<div className="bg-primary/10 absolute -top-16 -right-16 h-40 w-40 rounded-full opacity-0 blur-3xl transition-opacity duration-500 group-hover:opacity-100" />

							<div className="relative">
								<div className="flex items-center justify-between">
									<div className="bg-primary-100 text-primary dark:bg-primary-500/10 flex h-14 w-14 items-center justify-center rounded-xl transition-all duration-300 group-hover:scale-110">
										{feature.icon}
									</div>

									<span className="border-border text-t-muted rounded-full border px-3 py-1 text-xs font-medium">
										{feature.tag}
									</span>
								</div>

								<h3 className="text-t-primary mt-8 text-xl font-bold">
									{feature.title}
								</h3>

								<p className="text-t-muted mt-4 leading-7">{feature.description}</p>
							</div>

							{/* Index indicator */}

							<div className="text-border/40 absolute right-8 bottom-6 text-5xl font-bold">
								0{index + 1}
							</div>
						</div>
					))}
				</div>

				{/* Highlight Banner */}

				<div className="border-border bg-surface mt-20 rounded-2xl border p-10 shadow-md lg:p-14">
					<div className="grid gap-10 lg:grid-cols-[1fr_auto] lg:items-center">
						<div>
							<div className="flex items-center gap-3">
								<div className="bg-accent-100 text-accent-700 dark:bg-accent-500/10 dark:text-accent rounded-xl p-3">
									<Bot size={22} />
								</div>

								<p className="text-accent font-semibold">
									AI is an accelerator, not the foundation
								</p>
							</div>

							<h3 className="text-t-primary mt-6 font-['Space_Grotesk'] text-3xl font-bold">
								Deterministic systems first.
								<br />
								AI intelligence where it matters.
							</h3>

							<p className="text-t-muted mt-5 max-w-3xl text-lg leading-8">
								SignalOps avoids treating AI as a black-box parser. Reliable rules
								handle predictable scenarios while AI provides semantic
								understanding for unknown events and operational reasoning.
							</p>
						</div>

						<div className="flex justify-center">
							<div className="border-primary/20 bg-primary-100 dark:bg-primary-500/10 rounded-2xl border px-8 py-10 text-center">
								<div className="text-primary text-5xl font-bold">2</div>

								<p className="text-t-muted mt-2 text-sm font-semibold tracking-widest uppercase">
									Processing Layers
								</p>

								<div className="mt-6 space-y-2 text-sm">
									<div className="bg-surface text-t-primary rounded-xl px-5 py-3 font-semibold">
										Rule Engine
									</div>

									<div className="text-t-muted">↓</div>

									<div className="bg-surface text-t-primary rounded-xl px-5 py-3 font-semibold">
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
