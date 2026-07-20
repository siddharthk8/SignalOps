import { getCoreRowModel, useReactTable } from "@tanstack/react-table";

import DataTable from "@/components/Table/DataTable";
import DataTablePagination from "@/components/Table/DataTablePagination";
import { batchColumns } from "@/shared/utils/TableColumns";

import Empty from "./Empty";
import TableHeader from "./TableHeader";

function BatchesTable({ batches, total, pagination, setPagination, onRowClick }) {
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

	return (
		<DataTable
			table={table}
			header={<TableHeader total={total} />}
			empty={<Empty />}
			onRowClick={onRowClick}
			pagination={
				<DataTablePagination
					total={total}
					pageIndex={pagination.pageIndex}
					pageSize={pagination.pageSize}
					pageCount={table.getPageCount()}
					canNextPage={table.getCanNextPage()}
					canPreviousPage={table.getCanPreviousPage()}
					onNext={table.nextPage}
					onPrevious={table.previousPage}
					onFirst={table.firstPage}
					onLast={table.lastPage}
					onPageChange={table.setPageIndex}
					onPageSizeChange={table.setPageSize}
				/>
			}
		/>
	);
}

export default BatchesTable;
