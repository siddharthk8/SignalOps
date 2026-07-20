import { ChevronDown, ChevronUp } from "lucide-react";
import { useState } from "react";

function Collapsible({ header, children, className = "" }) {
	const [expanded, setExpanded] = useState(false);

	return (
		<div className={className}>
			<button
				onClick={() => setExpanded((prev) => !prev)}
				className="flex w-full items-start justify-between px-5 py-4 text-left"
			>
				{header}

				{expanded ? (
					<ChevronUp size={18} className="text-t-muted ml-4 shrink-0" />
				) : (
					<ChevronDown size={18} className="text-t-muted ml-4 shrink-0" />
				)}
			</button>

			{expanded && <div className="bg-muted/20 px-5 py-5">{children}</div>}
		</div>
	);
}

export default Collapsible;
