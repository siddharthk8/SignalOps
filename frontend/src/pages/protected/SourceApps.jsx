import { keepPreviousData, useQuery } from "@tanstack/react-query";
import { useState } from "react";
import { useNavigate } from "react-router";

import { getSourceApps } from "@/api";
import Container from "@/components/Container";
import Loader from "@/components/Loader";
import SourceAppsTable from "@/components/Pages/SourceApps/Table";
import QueryError from "@/components/QueryError";
import QueryPageHeader from "@/components/QueryPageHeader";
import authenticatedClient from "@/core/api/customClient";

function SourceAppsPage() {
	const navigate = useNavigate();

	const [pagination, setPagination] = useState({
		pageIndex: 0,
		pageSize: 10,
	});
	const [fetchAction, setFetchAction] = useState(null);

	const { data, isPending, isFetching, isError, refetch } = useQuery({
		queryKey: ["source-apps", pagination.pageIndex, pagination.pageSize],
		placeholderData: keepPreviousData,
		queryFn: async () => {
			try {
				return await getSourceApps({
					client: authenticatedClient,
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
				title="Source Applications"
				description="Manage applications connected to your SignalOps monitoring workspace."
				onRefresh={handleRefresh}
				isRefreshing={isRefreshing}
				isPaginationPageLoading={isPaginationPageLoading}
			/>

			<SourceAppsTable
				sourceApps={data.source_apps}
				total={data.total}
				pagination={pagination}
				setPagination={handlePaginationChange}
				onRowClick={(row) => navigate(`/dashboard/source-apps/${row.original.id}/batches`)}
			/>
		</Container>
	);
}

export default SourceAppsPage;
