import { keepPreviousData, useQuery } from "@tanstack/react-query";
import { flexRender, getCoreRowModel, useReactTable } from "@tanstack/react-table";
import {
	ChevronLeft,
	ChevronRight,
	ChevronsLeft,
	ChevronsRight,
	Database,
	Loader2,
} from "lucide-react";
import { useMemo, useState } from "react";
import { useNavigate, useParams } from "react-router";

import { getSourceAppBatches } from "@/api";
import Container from "@/components/Container";
import Loader from "@/components/Loader";
import QueryError from "@/components/QueryError";
import authenticatedClient from "@/core/api/customClient";
import getVisiblePages from "@/shared/utils/getVisiblePages";
import { batchColumns } from "@/shared/utils/TableColumns";

function BatchesPage() {
	const navigate = useNavigate();
	const { sourceAppId } = useParams();
	const [pagination, setPagination] = useState({
		pageIndex: 0,
		pageSize: 1,
	});

	const { data, isLoading, isFetching, isError, refetch } = useQuery({
		queryKey: ["batches", sourceAppId, pagination.pageIndex, pagination.pageSize],
		placeholderData: keepPreviousData,
		queryFn: () =>
			getSourceAppBatches({
				client: authenticatedClient,
				path: {
					source_app_id: Number(sourceAppId),
				},
				query: {
					skip: pagination.pageIndex * pagination.pageSize,
					limit: pagination.pageSize,
				},
			}),
	});

	const batches = data?.data?.batches ?? [];
	const total = data?.data?.total ?? 0;

	const table = useReactTable({
		data: batches,
		columns: batchColumns,
		getCoreRowModel: getCoreRowModel(),
		manualPagination: true,
		rowCount: total,

		state: {
			pagination,
		},

		onPaginationChange: setPagination,
	});

	const currentPage = table.getState().pagination.pageIndex + 1;
	const pageCount = table.getPageCount();

	const pages = useMemo(() => {
		return getVisiblePages(currentPage, pageCount);
	}, [currentPage, pageCount]);

	if (isLoading) {
		return <Loader />;
	}

	if (isError || !data) {
		return <QueryError onRetry={refetch} />;
	}

	return (
		<Container>
			<div className="space-y-8">
				{/* Header */}

				<section className="flex items-start justify-between">
					<div>
						<div className="flex items-center gap-3">
							<h1 className="font-['Space_Grotesk'] text-3xl font-bold">
								Batch History
							</h1>

							<span className="bg-primary/10 text-primary rounded-full px-3 py-1 text-xs font-bold">
								{total} Batches
							</span>
						</div>

						<p className="text-t-muted mt-2 text-sm">
							View historical ingestion batches processed by the semantic intelligence
							pipeline.
						</p>
					</div>

					{isFetching && <Loader2 size={20} className="text-primary animate-spin" />}
				</section>

				<section className="bg-surface border-border overflow-hidden rounded-3xl border">
					<div className="border-border flex items-center justify-between border-b px-6 py-5">
						<div>
							<h2 className="text-lg font-semibold">Ingestion Batches</h2>

							<p className="text-t-muted mt-1 text-sm">
								Historical log ingestion records
							</p>
						</div>

						<div className="bg-primary/10 text-primary flex h-11 w-11 items-center justify-center rounded-xl">
							<Database size={22} />
						</div>
					</div>

					{batches.length === 0 ? (
						<div className="flex flex-col items-center justify-center py-28">
							<div className="bg-primary/10 text-primary mb-6 flex h-18 w-18 items-center justify-center rounded-3xl">
								<Database size={34} />
							</div>

							<h3 className="text-xl font-semibold">No Batches Found</h3>

							<p className="text-t-muted mt-2 max-w-md text-center text-sm">
								This application hasn't ingested any log batches yet. Once logs are
								processed they'll appear here.
							</p>
						</div>
					) : (
						<>
							<div className="overflow-x-auto">
								<table className="w-full">
									<thead className="bg-elevated/40">
										{table.getHeaderGroups().map((headerGroup) => (
											<tr
												key={headerGroup.id}
												className="border-border border-b"
											>
												{headerGroup.headers.map((header) => (
													<th
														key={header.id}
														className="text-t-muted px-6 py-4 text-left text-xs font-semibold tracking-wider uppercase"
													>
														{flexRender(
															header.column.columnDef.header,
															header.getContext(),
														)}
													</th>
												))}

												<th className="w-16"></th>
											</tr>
										))}
									</thead>

									<tbody>
										{table.getRowModel().rows.map((row) => (
											<tr
												key={row.id}
												onClick={() => navigate(`${row.original.id}`)}
												className="border-border hover:bg-primary/5 group cursor-pointer border-b transition-all duration-200"
											>
												{row.getVisibleCells().map((cell) => (
													<td key={cell.id} className="px-6 py-5">
														{flexRender(
															cell.column.columnDef.cell,
															cell.getContext(),
														)}
													</td>
												))}

												<td className="px-6">
													<div className="text-primary flex justify-end opacity-0 transition-all duration-200 group-hover:translate-x-1 group-hover:opacity-100">
														<ChevronRight size={18} />
													</div>
												</td>
											</tr>
										))}
									</tbody>
								</table>
							</div>

							<div className="border-border flex flex-col gap-6 border-t px-6 py-5 xl:flex-row xl:items-center xl:justify-between">
								<div className="text-t-muted text-sm">
									Showing{" "}
									<span className="font-semibold">
										{total === 0
											? 0
											: pagination.pageIndex * pagination.pageSize + 1}
									</span>
									{" - "}
									<span className="font-semibold">
										{Math.min(
											(pagination.pageIndex + 1) * pagination.pageSize,
											total,
										)}
									</span>{" "}
									of <span className="font-semibold">{total}</span> batches
								</div>

								<div className="flex flex-wrap items-center gap-3">
									<button
										onClick={() => table.firstPage()}
										disabled={!table.getCanPreviousPage()}
										className="border-border hover:bg-elevated disabled:text-t-muted flex h-10 w-10 items-center justify-center rounded-lg border transition disabled:cursor-not-allowed disabled:opacity-50"
									>
										<ChevronsLeft size={18} />
									</button>

									<button
										onClick={() => table.previousPage()}
										disabled={!table.getCanPreviousPage()}
										className="border-border hover:bg-elevated disabled:text-t-muted flex h-10 w-10 items-center justify-center rounded-lg border transition disabled:cursor-not-allowed disabled:opacity-50"
									>
										<ChevronLeft size={18} />
									</button>

									{pages.map((page, index) => {
										if (page === "...") {
											return (
												<span key={index} className="text-t-muted px-2">
													...
												</span>
											);
										}

										return (
											<button
												key={page}
												onClick={() => table.setPageIndex(page)}
												disabled={page === pagination.pageIndex}
												className={`h-10 min-w-10 rounded-lg border px-3 text-sm font-medium transition ${
													page === pagination.pageIndex
														? "bg-primary border-primary text-white"
														: "border-border hover:bg-elevated"
												}`}
											>
												{page + 1}
											</button>
										);
									})}
									<button
										onClick={() => table.nextPage()}
										disabled={!table.getCanNextPage()}
										className="border-border hover:bg-elevated disabled:text-t-muted flex h-10 w-10 items-center justify-center rounded-lg border transition disabled:cursor-not-allowed disabled:opacity-50"
									>
										<ChevronRight size={18} />
									</button>

									<button
										onClick={() => table.lastPage()}
										disabled={!table.getCanNextPage()}
										className="border-border hover:bg-elevated disabled:text-t-muted flex h-10 w-10 items-center justify-center rounded-lg border transition disabled:cursor-not-allowed disabled:opacity-50"
									>
										<ChevronsRight size={18} />
									</button>

									<div className="bg-border mx-2 h-6 w-px" />

									<select
										value={pagination.pageSize}
										onChange={(e) =>
											table.setPagination({
												pageIndex: 0,
												pageSize: Number(e.target.value),
											})
										}
										className="border-border bg-surface rounded-lg border px-3 py-2 text-sm outline-none"
									>
										{[10, 20, 30, 50, 100].map((size) => (
											<option key={size} value={size}>
												Show {size}
											</option>
										))}
									</select>
								</div>
							</div>
						</>
					)}
				</section>
			</div>
		</Container>
	);
}

export default BatchesPage;
