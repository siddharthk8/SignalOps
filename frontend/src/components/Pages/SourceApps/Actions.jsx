import { AlertTriangle, ChevronRight, LoaderCircle, Trash2, X } from "lucide-react";
import { useState } from "react";

function Actions({ row, onDelete, isDeleting }) {
	const [showConfirm, setShowConfirm] = useState(false);

	const handleDelete = async (e) => {
		e.stopPropagation();

		try {
			await onDelete(row.original.id);
			setShowConfirm(false);
		} catch {
			// Keep the dialog open if deletion fails.
		}
	};

	return (
		<>
			<div className="flex items-center justify-end gap-2">
				<button
					type="button"
					title="Delete Source Application"
					aria-label="Delete Source Application"
					disabled={isDeleting}
					onClick={(e) => {
						e.stopPropagation();
						setShowConfirm(true);
					}}
					className="text-error hover:bg-error/10 active:bg-error/20 cursor-pointer rounded-lg p-2 transition-colors disabled:cursor-not-allowed disabled:opacity-50"
				>
					<Trash2 size={18} />
				</button>

				<ChevronRight
					size={18}
					className="text-primary shrink-0 cursor-default transition-transform group-hover:translate-x-1"
				/>
			</div>

			{showConfirm && (
				<div
					className="fixed inset-0 z-50 flex cursor-default items-center justify-center bg-black/50 p-4 backdrop-blur-sm"
					onClick={() => !isDeleting && setShowConfirm(false)}
				>
					<div
						role="alertdialog"
						aria-modal="true"
						aria-labelledby="delete-title"
						aria-describedby="delete-description"
						onClick={(e) => e.stopPropagation()}
						className="bg-surface border-border animate-in fade-in zoom-in-95 relative w-full max-w-sm cursor-default rounded-2xl border p-6 shadow-lg duration-200"
					>
						<button
							type="button"
							onClick={() => setShowConfirm(false)}
							disabled={isDeleting}
							aria-label="Close dialog"
							className="text-t-muted hover:text-t-primary hover:bg-elevated absolute top-4 right-4 cursor-pointer rounded-lg p-1.5 transition disabled:cursor-not-allowed disabled:opacity-50"
						>
							<X size={18} />
						</button>

						<div className="bg-error/10 text-error mb-4 flex h-12 w-12 items-center justify-center rounded-xl">
							<AlertTriangle size={24} />
						</div>

						<h2 id="delete-title" className="text-t-primary text-lg font-semibold">
							Delete Source Application?
						</h2>

						<p
							id="delete-description"
							className="text-t-muted mt-2 text-sm leading-relaxed"
						>
							Are you sure you want to delete this source application? This action
							cannot be undone.
						</p>

						<div className="mt-6 flex flex-col-reverse gap-2 sm:flex-row sm:justify-end">
							<button
								type="button"
								onClick={() => setShowConfirm(false)}
								disabled={isDeleting}
								className="border-border text-t-secondary hover:bg-elevated cursor-pointer rounded-lg border px-4 py-2.5 text-sm font-medium transition disabled:cursor-not-allowed disabled:opacity-50"
							>
								Cancel
							</button>

							<button
								type="button"
								onClick={handleDelete}
								disabled={isDeleting}
								className="bg-error inline-flex cursor-pointer items-center justify-center gap-2 rounded-lg px-4 py-2.5 text-sm font-medium text-white transition hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-60"
							>
								{isDeleting ? (
									<>
										<LoaderCircle size={16} className="animate-spin" />
										Deleting...
									</>
								) : (
									<>
										<Trash2 size={16} />
										Delete
									</>
								)}
							</button>
						</div>
					</div>
				</div>
			)}
		</>
	);
}

export default Actions;
