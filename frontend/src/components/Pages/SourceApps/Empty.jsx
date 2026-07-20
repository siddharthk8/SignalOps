import { Server } from "lucide-react";

function Empty() {
	return (
		<div className="flex flex-col items-center justify-center px-6 py-20 text-center">
			<div className="bg-primary/10 text-primary flex size-16 items-center justify-center rounded-full">
				<Server size={30} />
			</div>

			<h3 className="text-t-primary mt-6 text-xl font-semibold">No Source Applications</h3>

			<p className="text-t-muted mt-3 max-w-md text-sm leading-6">
				You haven't added any source applications yet. Create your first application to
				start collecting logs and monitoring incidents.
			</p>
		</div>
	);
}

export default Empty;
