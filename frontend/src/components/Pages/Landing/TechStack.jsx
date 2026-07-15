import { Award, Cloud, Code2, Database, Globe2, Layers, Server, Sparkles } from "lucide-react";

function TechStackSection() {
	const technologies = [
		{
			name: "FastAPI",
			category: "Backend Framework",
			description: "High-performance async APIs powering ingestion and platform services.",
			icon: <Server size={26} />,
		},
		{
			name: "Python",
			category: "Core Language",
			description: "The foundation for parsing, intelligence pipelines, and backend logic.",
			icon: <Code2 size={26} />,
		},
		{
			name: "SQLAlchemy",
			category: "Data Layer",
			description: "Structured ORM layer managing application intelligence data models.",
			icon: <Database size={26} />,
		},
		{
			name: "React",
			category: "Frontend",
			description: "Modern dashboard experience for operational visibility.",
			icon: <Globe2 size={26} />,
		},
		{
			name: "AWS Bedrock",
			category: "AI Engine",
			description: "Generative AI reasoning for incident analysis and recommendations.",
			icon: <Cloud size={26} />,
		},
		{
			name: "Semantic Pipeline",
			category: "Architecture",
			description: "Custom intelligence workflow transforming logs into incidents.",
			icon: <Layers size={26} />,
		},
	];

	return (
		<section id="technology" className="relative overflow-hidden bg-surface py-32">
			<div className="absolute inset-0">
				<div className="absolute right-1/3 top-0 h-[30rem] w-[30rem] rounded-full bg-primary/5 blur-[150px]" />
			</div>

			<div className="relative mx-auto max-w-7xl px-6">
				{/* Header */}

				<div className="mx-auto max-w-3xl text-center">
					<div className="inline-flex items-center gap-2 rounded-full border border-primary-300 bg-primary-100 px-4 py-2 text-sm font-semibold text-primary-700 dark:border-primary-500/20 dark:bg-primary-500/10 dark:text-primary-300">
						<Sparkles size={15} />
						Technology Foundation
					</div>

					<h2 className="mt-6 font-['Space_Grotesk'] text-4xl font-bold tracking-tight text-t-primary md:text-5xl">
						Built with modern
						<br />
						<span className="text-primary">engineering foundations.</span>
					</h2>

					<p className="mt-6 text-lg leading-8 text-t-muted">
						SignalOps combines reliable backend engineering with modern AI capabilities
						to create a scalable application log intelligence platform.
					</p>
				</div>

				{/* Technology Grid */}

				<div className="mt-20 grid gap-6 md:grid-cols-2 lg:grid-cols-3">
					{technologies.map((tech, index) => (
						<div
							key={tech.name}
							className="group relative overflow-hidden rounded-3xl border border-border bg-bg p-8 transition-all duration-500 hover:-translate-y-2 hover:border-primary/40 hover:shadow-lg"
						>
							<div className="absolute right-0 top-0 h-32 w-32 rounded-full bg-primary/5 blur-3xl transition-all duration-500 group-hover:bg-primary/10" />

							<div className="relative">
								<div className="flex items-start justify-between">
									<div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-primary-100 text-primary transition-transform duration-300 group-hover:scale-110 dark:bg-primary-500/10">
										{tech.icon}
									</div>

									<div className="text-5xl font-bold text-border/40">
										0{index + 1}
									</div>
								</div>

								<div className="mt-8">
									<p className="text-xs font-semibold uppercase tracking-[0.25em] text-primary">
										{tech.category}
									</p>

									<h3 className="mt-3 text-2xl font-bold text-t-primary">
										{tech.name}
									</h3>

									<p className="mt-4 leading-7 text-t-muted">
										{tech.description}
									</p>
								</div>
							</div>
						</div>
					))}
				</div>

				{/* Architecture Philosophy */}

				<div className="mt-20 overflow-hidden rounded-[2rem] border border-border bg-bg">
					<div className="grid lg:grid-cols-2">
						<div className="p-10 lg:p-14">
							<div className="flex items-center gap-3">
								<div className="rounded-xl bg-primary-100 p-3 text-primary dark:bg-primary-500/10">
									<Award size={22} />
								</div>

								<p className="font-semibold text-primary">Engineering Approach</p>
							</div>

							<h3 className="mt-6 font-['Space_Grotesk'] text-3xl font-bold leading-tight text-t-primary">
								Designed for clarity, reliability, and evolution.
							</h3>

							<p className="mt-5 text-lg leading-8 text-t-muted">
								Every component has a focused responsibility. Parsing, detection,
								correlation, persistence, and AI reasoning are separated into
								independent layers.
							</p>

							<p className="mt-5 text-lg leading-8 text-t-muted">
								This allows SignalOps to scale from simple log analysis into a
								complete operational intelligence platform.
							</p>
						</div>

						<div className="border-t border-border bg-surface p-10 lg:border-l lg:border-t-0 lg:p-14">
							<div className="space-y-4">
								<ArchitectureItem
									title="Deterministic First"
									description="Rules and parsers handle predictable scenarios."
								/>

								<ArchitectureItem
									title="AI Assisted"
									description="AI handles semantic uncertainty and reasoning."
								/>

								<ArchitectureItem
									title="Modular Design"
									description="Each pipeline stage can evolve independently."
								/>

								<ArchitectureItem
									title="Cloud Ready"
									description="Built on modern AWS-powered infrastructure."
								/>
							</div>
						</div>
					</div>
				</div>
			</div>
		</section>
	);
}

function ArchitectureItem({ title, description }) {
	return (
		<div className="rounded-2xl border border-border bg-bg p-5">
			<h4 className="font-bold text-t-primary">{title}</h4>

			<p className="mt-2 text-sm leading-6 text-t-muted">{description}</p>
		</div>
	);
}

export default TechStackSection;
