import { GitBranch, Sparkles } from "lucide-react";

function BottomSection() {
	return (
		<div className="border-border bg-surface relative overflow-hidden border-t">
			{/* Background */}

			<div className="absolute inset-0">
				<div className="bg-primary/10 absolute top-0 left-1/2 h-[30rem] w-[30rem] -translate-x-1/2 rounded-full blur-[160px]" />
			</div>

			<div className="relative mx-auto max-w-7xl px-6 pt-24">
				{/* Final CTA */}

				<div className="border-primary/20 bg-primary-100 dark:bg-primary-500/10 overflow-hidden rounded-[1.5rem] border">
					<div className="relative px-8 py-16 text-center lg:px-20 lg:py-20">
						<div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(6,182,212,0.12),transparent_45%)]" />

						<div className="relative mx-auto max-w-3xl">
							<div className="border-primary/20 bg-surface text-primary mx-auto flex w-fit items-center gap-2 rounded-full border px-4 py-2 text-sm font-semibold">
								<Sparkles size={15} />
								SignalOps Intelligence Platform
							</div>

							<h2 className="text-t-primary mt-8 font-['Space_Grotesk'] text-4xl font-bold tracking-tight md:text-6xl">
								Build systems that
								<br />
								<span className="text-primary">understand themselves.</span>
							</h2>

							<p className="text-t-muted mx-auto mt-6 max-w-2xl text-lg leading-8">
								SignalOps transforms application logs into semantic
								intelligence—helping engineers move from searching through noise to
								understanding what actually happened.
							</p>
						</div>
					</div>
				</div>

				{/* Bottom Content */}

				<div className="flex flex-col gap-10 py-12 lg:flex-row lg:items-center lg:justify-between">
					<div>
						<h3 className="text-t-primary font-['Space_Grotesk'] text-2xl font-bold">
							SignalOps
						</h3>

						<p className="text-t-muted mt-3 max-w-md text-sm leading-6">
							AI-powered application log intelligence platform for semantic event
							detection, incident correlation, and operational reasoning.
						</p>
					</div>

					<a
						href="https://github.com/siddharthk8/SignalOps"
						target="_blank"
						className="border-border bg-bg text-t-primary hover:border-primary flex items-center gap-3 rounded-xl border px-5 py-3 text-sm font-semibold transition"
					>
						<GitBranch size={18} />
						View Source
					</a>
				</div>
			</div>
		</div>
	);
}

export default BottomSection;
