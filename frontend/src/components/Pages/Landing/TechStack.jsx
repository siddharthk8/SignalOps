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
		<section id="technology" className="bg-surface relative overflow-hidden py-32">
			<div className="absolute inset-0">
				<div className="bg-primary/5 absolute top-0 right-1/3 h-[30rem] w-[30rem] rounded-full blur-[150px]" />
			</div>

			<div className="relative mx-auto max-w-7xl px-6">
				{/* Header */}

				<div className="mx-auto max-w-3xl text-center">
					<div className="border-primary-300 bg-primary-100 text-primary-700 dark:border-primary-500/20 dark:bg-primary-500/10 dark:text-primary-600 inline-flex items-center gap-2 rounded-full border px-4 py-2 text-sm font-semibold">
						<Sparkles size={15} />
						Technology Foundation
					</div>

					<h2 className="text-t-primary mt-6 font-['Space_Grotesk'] text-4xl font-bold tracking-tight md:text-5xl">
						Built with modern
						<br />
						<span className="text-primary">engineering foundations.</span>
					</h2>

					<p className="text-t-muted mt-6 text-lg leading-8">
						SignalOps combines reliable backend engineering with modern AI capabilities
						to create a scalable application log intelligence platform.
					</p>
				</div>

				{/* Technology Grid */}

				<div className="mt-20 grid gap-6 md:grid-cols-2 lg:grid-cols-3">
					{technologies.map((tech, index) => (
						<div
							key={tech.name}
							className="group border-border bg-bg hover:border-primary/40 relative overflow-hidden rounded-2xl border p-8 transition-all duration-500 hover:-translate-y-2 hover:shadow-lg"
						>
							<div className="bg-primary/5 group-hover:bg-primary/10 absolute top-0 right-0 h-32 w-32 rounded-full blur-3xl transition-all duration-500" />

							<div className="relative">
								<div className="flex items-start justify-between">
									<div className="bg-primary-100 text-primary dark:bg-primary-500/10 flex h-14 w-14 items-center justify-center rounded-2xl transition-transform duration-300 group-hover:scale-110">
										{tech.icon}
									</div>

									<div className="text-border/40 text-5xl font-bold">
										0{index + 1}
									</div>
								</div>

								<div className="mt-8">
									<p className="text-primary text-xs font-semibold tracking-[0.25em] uppercase">
										{tech.category}
									</p>

									<h3 className="text-t-primary mt-3 text-2xl font-bold">
										{tech.name}
									</h3>

									<p className="text-t-muted mt-4 leading-7">
										{tech.description}
									</p>
								</div>
							</div>
						</div>
					))}
				</div>

				{/* Architecture Philosophy */}

				<div className="border-border bg-bg mt-20 overflow-hidden rounded-2xl border">
					<div className="grid lg:grid-cols-2">
						<div className="p-10 lg:p-14">
							<div className="flex items-center gap-3">
								<div className="bg-primary-100 text-primary dark:bg-primary-500/10 rounded-xl p-3">
									<Award size={22} />
								</div>

								<p className="text-primary font-semibold">Engineering Approach</p>
							</div>

							<h3 className="text-t-primary mt-6 font-['Space_Grotesk'] text-3xl leading-tight font-bold">
								Designed for clarity, reliability, and evolution.
							</h3>

							<p className="text-t-muted mt-5 text-lg leading-8">
								Every component has a focused responsibility. Parsing, detection,
								correlation, persistence, and AI reasoning are separated into
								independent layers.
							</p>

							<p className="text-t-muted mt-5 text-lg leading-8">
								This allows SignalOps to scale from simple log analysis into a
								complete operational intelligence platform.
							</p>
						</div>

						<div className="border-border bg-surface border-t p-10 lg:border-t-0 lg:border-l lg:p-14">
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
		<div className="border-border bg-bg rounded-2xl border p-5">
			<h4 className="text-t-primary font-bold">{title}</h4>

			<p className="text-t-muted mt-2 text-sm leading-6">{description}</p>
		</div>
	);
}

export default TechStackSection;
