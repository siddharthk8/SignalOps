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
	const [fetchAction, setFetchAction] = useState(null);

	const { data, isPending, isFetching, isError, refetch } = useQuery({
		queryKey: ["batches", sourceAppId, pagination.pageIndex, pagination.pageSize],
		placeholderData: keepPreviousData,
		queryFn: async () => {
			try {
				return await getSourceAppBatches({
					client: authenticatedClient,
					path: {
						source_app_id: Number(sourceAppId),
					},
					query: {
						skip: pagination.pageIndex * pagination.pageSize,
						limit: pagination.pageSize,
					},
				});
			} finally {
				setFetchAction(null);
			}
		},
		select: (response) => response.data,
	});

	const handleRefresh = () => {
		setFetchAction("refresh");
		refetch();
	};

	const handlePaginationChange = (updater) => {
		setFetchAction("pagination");
		setPagination(updater);
	};

	const isRefreshing = fetchAction === "refresh" && isFetching;
	const isPaginationPageLoading = fetchAction === "pagination" && isFetching;

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
				onRefresh={handleRefresh}
				isRefreshing={isRefreshing}
				isPaginationPageLoading={isPaginationPageLoading}
				actions={
					<Button
						variant="success"
						onClick={() => navigate(`/source-apps/${sourceAppId}/ingestion`)}
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
				setPagination={handlePaginationChange}
				onRowClick={(row) => navigate(`${row.original.id}`)}
			/>
		</Container>
	);
}

export default BatchesPage;
