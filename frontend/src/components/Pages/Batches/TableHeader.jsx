import { Database } from "lucide-react";

function BatchesTableHeader({ total }) {
	return (
		<div className="border-border flex items-center justify-between border-b px-6 py-5">
			<div>
				<h2 className="text-t-primary text-lg font-semibold">Ingestion Batches</h2>

				<p className="text-t-muted mt-1 text-sm">
					{total} {total === 1 ? "batch" : "batches"} processed
				</p>
			</div>

			<div className="bg-primary/10 text-primary flex size-11 items-center justify-center rounded-lg">
				<Database size={22} />
			</div>
		</div>
	);
}

export default BatchesTableHeader;
