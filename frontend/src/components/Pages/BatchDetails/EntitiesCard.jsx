import {
	ChevronDown,
	ChevronUp,
	Globe,
	Hash,
	KeyRound,
	Mail,
	Monitor,
	User,
	Users,
} from "lucide-react";
import { useState } from "react";

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
	const [expanded, setExpanded] = useState(false);

	const availableFields = fields.filter(({ key }) => entity[key]);

	return (
		<div className="border-border hover:bg-muted/20 border-b last:border-b-0">
			<button
				onClick={() => setExpanded((prev) => !prev)}
				className="flex w-full items-center justify-between px-5 py-4 text-left"
			>
				<div className="min-w-0 flex-1">
					<div className="mb-2 flex items-center gap-3">
						<div className="bg-primary/10 text-primary flex h-8 w-8 items-center justify-center rounded-md">
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

				{expanded ? (
					<ChevronUp size={18} className="text-t-muted ml-4 shrink-0" />
				) : (
					<ChevronDown size={18} className="text-t-muted ml-4 shrink-0" />
				)}
			</button>

			{expanded && (
				<div className="border-border bg-muted/20 border-t px-5 py-5">
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
				</div>
			)}
		</div>
	);
}

function EntitiesCard({ entities }) {
	const [showAll, setShowAll] = useState(false);

	const visibleEntities = showAll ? entities : entities.slice(0, 5);

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
				<>
					<div>
						{visibleEntities.map((entity) => (
							<EntityRow key={entity.id} entity={entity} />
						))}
					</div>

					{entities.length > 5 && (
						<div className="border-border border-t px-5 py-3">
							<button
								onClick={() => setShowAll((prev) => !prev)}
								className="text-primary hover:text-primary/80 flex items-center gap-2 text-sm font-medium"
							>
								{showAll ? (
									<>
										<ChevronUp size={16} />
										Show Less
									</>
								) : (
									<>
										<ChevronDown size={16} />
										Show All ({entities.length})
									</>
								)}
							</button>
						</div>
					)}
				</>
			)}
		</section>
	);
}

export default EntitiesCard;
