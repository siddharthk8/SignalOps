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

	const { data, isPending, isFetching, isError, refetch } = useQuery({
		queryKey: ["source-apps", pagination.pageIndex, pagination.pageSize],
		placeholderData: keepPreviousData,
		queryFn: () =>
			getSourceApps({
				client: authenticatedClient,
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
		<Container>
			<div className="space-y-8">
				<QueryPageHeader
					title="Source Applications"
					description="Manage applications connected to your SignalOps monitoring workspace."
					onRefresh={refetch}
					isRefreshing={isFetching}
				/>

				<SourceAppsTable
					sourceApps={data.source_apps}
					total={data.total}
					pagination={pagination}
					setPagination={setPagination}
					onRowClick={(row) =>
						navigate(`/dashboard/source-apps/${row.original.id}/batches`)
					}
				/>
			</div>
		</Container>
	);
}

export default SourceAppsPage;
