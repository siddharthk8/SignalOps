import { SourceAppModel } from "@/api";
import { createColumnHelper } from "@tanstack/react-table";

const columnHelper = createColumnHelper<SourceAppModel>();

export const sourceAppTableColumns = [
	columnHelper.accessor("id", {
		header: "ID",
	}),
	columnHelper.accessor("name", {
		header: "Name",
		cell: ({ getValue }) => {
			return <strong>{getValue()}</strong>;
		},
	}),
	columnHelper.accessor("app_type", {
		header: "App Type",
	}),
	columnHelper.accessor((row) => new Date(row.created_at).toLocaleDateString(), {
		id: "createdDate",
		header: "Created Date",
	}),
	columnHelper.accessor((row) => new Date(row.created_at).toLocaleTimeString(), {
		id: "createdTime",
		header: "Created Time",
	}),
];
