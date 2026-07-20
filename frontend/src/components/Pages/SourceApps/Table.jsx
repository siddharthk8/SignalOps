import { useMutation, useQueryClient } from "@tanstack/react-query";
import { getCoreRowModel, useReactTable } from "@tanstack/react-table";

import { deleteSourceApp } from "@/api";
import DataTable from "@/components/Table/DataTable";
import DataTablePagination from "@/components/Table/DataTablePagination";
import authenticatedClient from "@/core/api/customClient";
import { sourceAppTableColumns } from "@/shared/utils/TableColumns";

import Actions from "./Actions";
import Empty from "./Empty";
import TableHeader from "./TableHeader";

function SourceAppsTable({ sourceApps, total, pagination, setPagination, onRowClick }) {
	const queryClient = useQueryClient();

	const { mutate: deleteApp, isPending: isDeleting } = useMutation({
		mutationFn: (sourceAppId) =>
			deleteSourceApp({
				client: authenticatedClient,
				path: {
					source_app_id: sourceAppId,
				},
			}),
		onSuccess: () => {
			queryClient.invalidateQueries({
				queryKey: ["source-apps"],
			});
		},
	});

	const table = useReactTable({
		data: sourceApps,
		columns: sourceAppTableColumns,
		getCoreRowModel: getCoreRowModel(),
		manualPagination: true,
		rowCount: total,
		state: {
			pagination,
		},
		onPaginationChange: setPagination,
	});

	return (
		<>
			<DataTable
				table={table}
				header={<TableHeader total={total} />}
				empty={<Empty />}
				pagination={
					<DataTablePagination
						total={total}
						pageIndex={pagination.pageIndex}
						pageSize={pagination.pageSize}
						pageCount={table.getPageCount()}
						canPreviousPage={table.getCanPreviousPage()}
						canNextPage={table.getCanNextPage()}
						onFirst={table.firstPage}
						onPrevious={table.previousPage}
						onNext={table.nextPage}
						onLast={table.lastPage}
						onPageChange={table.setPageIndex}
						onPageSizeChange={(size) => {
							table.setPageSize(size);
							table.setPageIndex(0);
						}}
					/>
				}
				onRowClick={onRowClick}
				rowActions={(row) => (
					<Actions row={row} onDelete={deleteApp} isDeleting={isDeleting} />
				)}
			/>
		</>
	);
}

export default SourceAppsTable;
