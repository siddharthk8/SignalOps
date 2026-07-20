import { keepPreviousData, useQuery } from "@tanstack/react-query";
import { Plus } from "lucide-react";
import { useState } from "react";
import { useNavigate, useParams } from "react-router";

import { getSourceAppBatches } from "@/api";
import Button from "@/components/Button";
import Container from "@/components/Container";
import Loader from "@/components/Loader";
import BatchesTable from "@/components/Pages/Batches/Table";
import QueryError from "@/components/QueryError";
import QueryPageHeader from "@/components/QueryPageHeader";
import authenticatedClient from "@/core/api/customClient";

function BatchesPage() {
	const navigate = useNavigate();
	const { sourceAppId } = useParams();

	const [pagination, setPagination] = useState({
		pageIndex: 0,
		pageSize: 10,
	});

	const { data, isPending, isFetching, isError, refetch } = useQuery({
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
		select: (response) => response.data,
	});

	if (isPending) {
		return <Loader />;
	}

	if (isError) {
		return <QueryError onRetry={refetch} />;
	}

	return (
		<Container className="space-y-8">
			<QueryPageHeader
				title="Batch History"
				description="Review historical log ingestion batches processed for this application."
				onRefresh={refetch}
				isRefreshing={isFetching}
				actions={
					<Button
						variant="success"
						onClick={() => navigate("ingest-logs")}
						rightIcon={<Plus size={16} />}
					>
						Ingest Logs
					</Button>
				}
			/>

			<BatchesTable
				batches={data.batches}
				total={data.total}
				pagination={pagination}
				setPagination={setPagination}
				onRowClick={(row) => navigate(`${row.original.id}`)}
			/>
		</Container>
	);
}

export default BatchesPage;
