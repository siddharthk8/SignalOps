import { ChevronLeft, ChevronRight, ChevronsLeft, ChevronsRight } from "lucide-react";

import getVisiblePages from "@/shared/utils/getVisiblePages";

function DataTablePagination({
	total,
	pageIndex,
	pageSize,
	pageCount,
	canPreviousPage,
	canNextPage,
	onFirst,
	onPrevious,
	onNext,
	onLast,
	onPageChange,
	onPageSizeChange,
	pageSizeOptions = [10, 20, 30, 50, 100],
}) {
	const pages = getVisiblePages(pageIndex + 1, pageCount);

	const from = total === 0 ? 0 : pageIndex * pageSize + 1;
	const to = Math.min((pageIndex + 1) * pageSize, total);

	return (
		<div className="border-border flex flex-col gap-6 border-t px-6 py-5 lg:flex-row lg:items-center lg:justify-between">
			<p className="text-t-muted text-sm">
				Showing <span className="text-t-primary font-semibold">{from}</span> –{" "}
				<span className="text-t-primary font-semibold">{to}</span> of{" "}
				<span className="text-t-primary font-semibold">{total}</span>
			</p>

			<div className="flex flex-wrap items-center gap-2">
				<button
					type="button"
					onClick={onFirst}
					disabled={!canPreviousPage}
					className="border-border hover:bg-elevated flex size-10 items-center justify-center rounded-lg border transition disabled:pointer-events-none disabled:opacity-50"
				>
					<ChevronsLeft size={18} />
				</button>

				<button
					type="button"
					onClick={onPrevious}
					disabled={!canPreviousPage}
					className="border-border hover:bg-elevated flex size-10 items-center justify-center rounded-lg border transition disabled:pointer-events-none disabled:opacity-50"
				>
					<ChevronLeft size={18} />
				</button>

				{pages.map((page, index) =>
					page === "..." ? (
						<span
							key={`ellipsis-${index}`}
							className="text-t-muted flex h-10 min-w-10 items-center justify-center"
						>
							...
						</span>
					) : (
						<button
							key={page}
							type="button"
							onClick={() => onPageChange(page)}
							className={`h-10 min-w-10 rounded-lg border px-3 text-sm font-medium transition ${
								page === pageIndex
									? "bg-primary border-primary text-white"
									: "border-border hover:bg-elevated"
							}`}
						>
							{page + 1}
						</button>
					),
				)}

				<button
					type="button"
					onClick={onNext}
					disabled={!canNextPage}
					className="border-border hover:bg-elevated flex size-10 items-center justify-center rounded-lg border transition disabled:pointer-events-none disabled:opacity-50"
				>
					<ChevronRight size={18} />
				</button>

				<button
					type="button"
					onClick={onLast}
					disabled={!canNextPage}
					className="border-border hover:bg-elevated flex size-10 items-center justify-center rounded-lg border transition disabled:pointer-events-none disabled:opacity-50"
				>
					<ChevronsRight size={18} />
				</button>

				<div className="bg-border mx-2 hidden h-6 w-px md:block" />

				<select
					value={pageSize}
					onChange={(e) => onPageSizeChange(Number(e.target.value))}
					className="border-border bg-surface rounded-lg border px-3 py-2 text-sm outline-none"
				>
					{pageSizeOptions.map((size) => (
						<option key={size} value={size}>
							Show {size}
						</option>
					))}
				</select>
			</div>
		</div>
	);
}

export default DataTablePagination;
