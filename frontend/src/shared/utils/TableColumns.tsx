import { Batch, SourceAppModel } from "@/api";
import { createColumnHelper } from "@tanstack/react-table";

const sourceAppColumnHelper = createColumnHelper<SourceAppModel>();

export const sourceAppTableColumns = [
	// sourceAppColumnHelper.accessor("id", {
	// 	header: "ID",
	// }),
	sourceAppColumnHelper.accessor("name", {
		header: "Name",
		cell: ({ getValue }) => {
			return <strong>{getValue()}</strong>;
		},
	}),
	sourceAppColumnHelper.accessor("app_type", {
		header: "App Type",
		cell: ({ getValue }) => {
			return getValue().replace(/-app$/, "");
		},
	}),
	sourceAppColumnHelper.accessor(
		(row) =>
			new Date(row.created_at).toLocaleDateString([], {
				month: "long",
				day: "numeric",
				year: "numeric",
			}),
		{
			id: "createdDate",
			header: "Creation Date",
		},
	),
	sourceAppColumnHelper.accessor(
		(row) =>
			new Date(row.created_at).toLocaleTimeString([], {
				hour: "2-digit",
				minute: "2-digit",
			}),
		{
			id: "createdTime",
			header: "Creation Time",
		},
	),
];

const batchColumnHelper = createColumnHelper<Batch>();

export const batchColumns = [
	// batchColumnHelper.accessor("id", {
	// 	header: "Batch ID",
	// }),
	batchColumnHelper.accessor("log_count", {
		header: "Total Logs",
	}),
	batchColumnHelper.accessor("created_at", {
		header: "Created At",
		cell: (info) => {
			const date = new Date(info.getValue());

			const formattedDate = date.toLocaleDateString([], {
				month: "long",
				day: "numeric",
				year: "numeric",
			});

			const formattedTime = date.toLocaleTimeString([], {
				hour: "2-digit",
				minute: "2-digit",
			});

			return `${formattedDate} - ${formattedTime}`;
		},
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
							<span className="font-medium">{analysis.severity.toUpperCase()}</span> (
							{Math.round(analysis.confidence * 100)}%)
						</div>
					))}
				</div>
			);
		},
	}),
];
