import { ChevronDown, ChevronUp } from "lucide-react";
import { useState } from "react";

function ExpandableList({ items, limit = 5, renderItem }) {
	const [expanded, setExpanded] = useState(false);

	const visibleItems = expanded ? items : items.slice(0, limit);

	return (
		<>
			<div>{visibleItems.map(renderItem)}</div>

			{items.length > limit && (
				<div className="border-border border-t px-5 py-3">
					<button
						onClick={() => setExpanded((prev) => !prev)}
						className="text-primary hover:text-primary/80 flex items-center gap-2 text-sm font-medium"
					>
						{expanded ? (
							<>
								<ChevronUp size={16} />
								Show Less
							</>
						) : (
							<>
								<ChevronDown size={16} />
								Show All ({items.length})
							</>
						)}
					</button>
				</div>
			)}
		</>
	);
}

export default ExpandableList;
