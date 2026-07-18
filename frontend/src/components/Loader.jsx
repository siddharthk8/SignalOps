import { Loader2 } from "lucide-react";

function Loader() {
	return (
		<div className="bg-bg/80 fixed inset-0 z-[9999] flex items-center justify-center backdrop-blur-sm">
			<div className="flex flex-col items-center gap-4">
				<div className="bg-surface border-border rounded-2xl border p-5 shadow-lg">
					<Loader2 className="text-primary h-10 w-10 animate-spin" />
				</div>

				<p className="text-t-muted text-sm font-medium">Loading...</p>
			</div>
		</div>
	);
}

export default Loader;
