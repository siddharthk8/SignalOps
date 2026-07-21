import { flexRender } from "@tanstack/react-table";

function DataTable({ table, header, pagination, empty, rowActions, onRowClick }) {
	return (
		<section className="border-border bg-surface overflow-hidden rounded-lg border">
			{header}

			{table.getRowModel().rows.length === 0 ? (
				empty
			) : (
				<>
					<div className="overflow-x-auto">
						<table className="w-full">
							<thead className="bg-elevated/40">
								{table.getHeaderGroups().map((headerGroup) => (
									<tr key={headerGroup.id} className="border-border border-b">
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

										{rowActions && <th className="w-16" />}
									</tr>
								))}
							</thead>

							<tbody>
								{table.getRowModel().rows.map((row) => (
									<tr
										key={row.id}
										onClick={() => onRowClick?.(row)}
										className={`border-border border-b transition-colors ${
											onRowClick
												? "hover:bg-primary/5 group cursor-pointer"
												: ""
										}`}
									>
										{row.getVisibleCells().map((cell) => (
											<td key={cell.id} className="px-6 py-5">
												{flexRender(
													cell.column.columnDef.cell,
													cell.getContext(),
												)}
											</td>
										))}

										{rowActions && (
											<td className="px-6">
												<div className="flex justify-end">
													{rowActions(row)}
												</div>
											</td>
										)}
									</tr>
								))}
							</tbody>
						</table>
					</div>

					{pagination}
				</>
			)}
		</section>
	);
}

export default DataTable;
