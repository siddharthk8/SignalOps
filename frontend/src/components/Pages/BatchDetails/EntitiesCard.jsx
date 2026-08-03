import { Globe, Hash, KeyRound, Mail, Monitor, User, Users } from "lucide-react";

import Collapsible from "@/components/Collapsible";
import ExpandableList from "@/components/ExpandableList";

const fields = [
	{
		key: "user",
		label: "User",
		icon: User,
	},
	{
		key: "email",
		label: "Email",
		icon: Mail,
	},
	{
		key: "ip_address",
		label: "IP Address",
		icon: Globe,
	},
	{
		key: "session_id",
		label: "Session",
		icon: Monitor,
	},
	{
		key: "token_id",
		label: "Token",
		icon: KeyRound,
	},
	{
		key: "request_id",
		label: "Request",
		icon: Hash,
	},
];

function EntityRow({ entity }) {
	const availableFields = fields.filter(({ key }) => entity[key]);

	return (
		<Collapsible
			className="border-border hover:bg-muted/20 border-t last:border-b-0"
			header={
				<div className="min-w-0 flex-1">
					<div className="mb-2 flex items-center gap-3">
						<div className="bg-accent/10 text-accent flex h-8 w-8 items-center justify-center rounded-md">
							<User size={15} />
						</div>

						<div>
							<div className="font-medium">Entity #{entity.id}</div>

							<div className="text-t-muted text-xs">Normalized Identity</div>
						</div>
					</div>

					<div className="flex flex-wrap gap-2">
						{availableFields.map(({ key, label }) => (
							<span
								key={key}
								className="bg-muted text-t-muted rounded px-2 py-1 text-[11px]"
							>
								<strong>{label}:</strong> {entity[key]}
							</span>
						))}
					</div>
				</div>
			}
		>
			<div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
				{fields.map(({ key, label, icon: Icon }) => (
					<div key={key} className="flex items-start gap-3">
						<Icon size={15} className="text-t-muted mt-0.5 shrink-0" />

						<div className="min-w-0">
							<div className="text-t-muted text-[11px] tracking-wide uppercase">
								{label}
							</div>

							<div className="text-sm font-medium break-all">
								{entity[key] || "—"}
							</div>
						</div>
					</div>
				))}
			</div>
		</Collapsible>
	);
}

function EntitiesCard({ entities }) {
	return (
		<section className="bg-surface border-border overflow-hidden rounded-md border">
			<div className="border-border flex items-center justify-between border-b px-5 py-4">
				<div>
					<h2 className="text-base font-semibold">Extracted Entities</h2>

					<p className="text-t-muted mt-1 text-sm">
						Normalized identities discovered during semantic parsing.
					</p>
				</div>

				<div className="bg-accent/10 text-accent flex h-9 w-9 items-center justify-center rounded-md">
					<Users size={18} />
				</div>
			</div>

			{entities.length === 0 ? (
				<div className="px-5 py-12 text-center">
					<Users size={28} className="text-t-muted mx-auto mb-3" />

					<h3 className="font-medium">No entities found</h3>

					<p className="text-t-muted mt-2 text-sm">
						No normalized identities were extracted.
					</p>
				</div>
			) : (
				<ExpandableList
					items={entities}
					limit={5}
					renderItem={(entity) => <EntityRow key={entity.id} entity={entity} />}
				/>
			)}
		</section>
	);
}

export default EntitiesCard;
