import { ChevronRight, Trash2 } from "lucide-react";

function Actions({ row, onDelete, isDeleting }) {
	return (
		<div className="flex items-center justify-end gap-3 opacity-0 transition-opacity group-hover:opacity-100">
			<button
				type="button"
				title="Delete Source Application"
				disabled={isDeleting}
				onClick={(e) => {
					e.stopPropagation();
					onDelete(row.original.id);
				}}
				className="text-error hover:bg-error/10 rounded-lg p-2 transition disabled:cursor-not-allowed disabled:opacity-50"
			>
				<Trash2 size={18} />
			</button>

			<ChevronRight
				size={18}
				className="text-primary transition-transform group-hover:translate-x-1"
			/>
		</div>
	);
}

export default Actions;
