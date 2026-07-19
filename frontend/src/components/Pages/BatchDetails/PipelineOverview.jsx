import { BrainCircuit, Database, FileText, ShieldAlert, Siren, Sparkles } from "lucide-react";

const stages = [
	{
		key: "logs",
		title: "Logs",
		icon: FileText,
		color: "text-info",
		bg: "bg-info/10",
	},
	{
		key: "entities",
		title: "Entities",
		icon: Database,
		color: "text-accent",
		bg: "bg-accent/10",
	},
	{
		key: "events",
		title: "Events",
		icon: Sparkles,
		color: "text-primary",
		bg: "bg-primary/10",
	},
	{
		key: "signals",
		title: "Signals",
		icon: Siren,
		color: "text-warning",
		bg: "bg-warning/10",
	},
	{
		key: "incidents",
		title: "Incidents",
		icon: ShieldAlert,
		color: "text-error",
		bg: "bg-error/10",
	},
	{
		key: "analysis",
		title: "AI Analysis",
		icon: BrainCircuit,
		color: "text-success",
		bg: "bg-success/10",
	},
];

function PipelineOverview() {
	return (
		<section className="bg-surface border-border rounded-md border">
			<div className="border-border border-b px-5 py-4">
				<h2 className="text-base font-semibold">Semantic Intelligence Pipeline</h2>

				<p className="text-t-muted mt-1 text-sm">
					Processing stages executed for this ingestion batch.
				</p>
			</div>

			<div className="overflow-x-auto">
				<div className="flex min-w-max items-center px-8 py-8">
					{stages.map((stage, index) => {
						const Icon = stage.icon;

						return (
							<div key={stage.key} className="flex items-center">
								<div className="flex w-28 flex-col items-center">
									<div
										className={`${stage.bg} border-border flex h-12 w-12 items-center justify-center rounded-md border`}
									>
										<Icon size={20} className={stage.color} />
									</div>

									<div className="mt-3 text-center text-sm font-medium">
										{stage.title}
									</div>
								</div>

								{index !== stages.length - 1 && (
									<div className="bg-border mx-3 h-px w-14" />
								)}
							</div>
						);
					})}
				</div>
			</div>
		</section>
	);
}

export default PipelineOverview;
