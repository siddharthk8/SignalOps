import { Loader2 } from "lucide-react";

function Loader() {
	return (
		<div className="absolute inset-0 flex items-center justify-center">
			<div className="flex flex-col items-center gap-4">
				<div className="relative flex h-14 w-14 items-center justify-center">
					<div className="bg-primary/20 absolute inset-0 animate-ping rounded-full" />

					<div className="bg-surface border-border relative flex h-12 w-12 items-center justify-center rounded-full border shadow-sm">
						<Loader2
							className="text-primary animate-spin"
							size={22}
							strokeWidth={2.5}
						/>
					</div>
				</div>

				<div className="text-center">
					<p className="text-t-primary text-sm font-medium">Loading...</p>
				</div>
			</div>
		</div>
	);
}

export default Loader;
