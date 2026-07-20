import { Database } from "lucide-react";

function EmptyBatches() {
	return (
		<div className="flex flex-col items-center justify-center px-6 py-24 text-center">
			<div className="bg-primary/10 text-primary mb-5 flex size-16 items-center justify-center rounded-2xl">
				<Database size={30} />
			</div>

			<h3 className="text-t-primary text-xl font-semibold">No batches yet</h3>

			<p className="text-t-muted mt-2 max-w-md text-sm leading-6">
				This application hasn't processed any log ingestion batches yet. Once logs are
				ingested, they'll appear here automatically.
			</p>
		</div>
	);
}

export default EmptyBatches;
