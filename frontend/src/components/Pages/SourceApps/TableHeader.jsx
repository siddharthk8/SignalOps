import { Server } from "lucide-react";

function TableHeader({ total }) {
	return (
		<div className="border-border flex items-center justify-between border-b px-6 py-5">
			<div>
				<h2 className="text-t-primary text-lg font-semibold">Application Registry</h2>

				<p className="text-t-muted mt-1 text-sm">
					{total > 0
						? `${total} registered application${total === 1 ? "" : "s"}`
						: "Registered source applications"}
				</p>
			</div>

			<div className="bg-primary/10 text-primary flex size-11 items-center justify-center rounded-lg">
				<Server size={22} />
			</div>
		</div>
	);
}

export default TableHeader;
