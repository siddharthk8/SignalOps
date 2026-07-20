import { BrainCircuit, Database, FileText, ShieldAlert, Siren, Sparkles } from "lucide-react";

const cards = [
	{
		key: "logs",
		title: "Raw Logs",
		icon: FileText,
		color: "text-slate-600 dark:text-slate-400",
		bg: "bg-slate-500/10",
	},
	{
		key: "entities",
		title: "Entities",
		icon: Database,
		color: "text-sky-600 dark:text-sky-400",
		bg: "bg-sky-500/10",
	},
	{
		key: "events",
		title: "Semantic Events",
		icon: Sparkles,
		color: "text-violet-600 dark:text-violet-400",
		bg: "bg-violet-500/10",
	},
	{
		key: "signals",
		title: "Signals",
		icon: Siren,
		color: "text-amber-600 dark:text-amber-400",
		bg: "bg-amber-500/10",
	},
	{
		key: "incidents",
		title: "Incidents",
		icon: ShieldAlert,
		color: "text-red-600 dark:text-red-400",
		bg: "bg-red-500/10",
	},
	{
		key: "analyses",
		title: "AI Analyses",
		icon: BrainCircuit,
		color: "text-emerald-600 dark:text-emerald-400",
		bg: "bg-emerald-500/10",
	},
];

function BatchOverviewCards({ overview }) {
	return (
		<section className="border-border bg-border grid gap-px overflow-hidden rounded-md border sm:grid-cols-2 lg:grid-cols-3">
			{cards.map(({ key, title, icon: Icon, color, bg }) => (
				<div key={key} className="bg-surface hover:bg-muted/30 group p-6 transition-colors">
					<div className="mb-6 flex items-center justify-between">
						<div>
							<p className="text-t-muted text-[11px] font-semibold tracking-[0.18em] uppercase">
								{title}
							</p>
						</div>

						<div
							className={`border-border ${bg} flex h-10 w-10 items-center justify-center rounded-md border`}
						>
							<Icon size={18} strokeWidth={1.8} className={color} />
						</div>
					</div>

					<div>
						<h2 className="text-4xl font-semibold tracking-tight">
							{Number(overview[key] ?? 0).toLocaleString()}
						</h2>

						<p className="text-t-muted mt-2 text-sm">Records processed</p>
					</div>
				</div>
			))}
		</section>
	);
}

export default BatchOverviewCards;
