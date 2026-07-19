import { Batch, SourceAppModel } from "@/api";
import { createColumnHelper } from "@tanstack/react-table";

const sourceAppColumnHelper = createColumnHelper<SourceAppModel>();

export const sourceAppTableColumns = [
	sourceAppColumnHelper.accessor("id", {
		header: "ID",
	}),
	sourceAppColumnHelper.accessor("name", {
		header: "Name",
		cell: ({ getValue }) => {
			return <strong>{getValue()}</strong>;
		},
	}),
	sourceAppColumnHelper.accessor("app_type", {
		header: "App Type",
	}),
	sourceAppColumnHelper.accessor((row) => new Date(row.created_at).toLocaleDateString(), {
		id: "createdDate",
		header: "Created Date",
	}),
	sourceAppColumnHelper.accessor((row) => new Date(row.created_at).toLocaleTimeString(), {
		id: "createdTime",
		header: "Created Time",
	}),
];

const batchColumnHelper = createColumnHelper<Batch>();

export const batchColumns = [
	batchColumnHelper.accessor("id", {
		header: "Batch ID",
	}),

	batchColumnHelper.accessor("log_count", {
		header: "Logs",
	}),

	batchColumnHelper.accessor("created_at", {
		header: "Created At",
		cell: (info) => new Date(info.getValue()).toLocaleString(),
	}),

	batchColumnHelper.accessor("ai_analyses", {
		header: "AI Analyses",
		cell: (info) => {
			const analyses = info.getValue();

			if (!analyses.length) {
				return "-";
			}

			return (
				<div className="space-y-1">
					{analyses.map((analysis) => (
						<div key={analysis.id} className="text-sm">
							<span className="font-medium">{analysis.severity}</span> (
							{Math.round(analysis.confidence * 100)}%)
						</div>
					))}
				</div>
			);
		},
	}),
];
