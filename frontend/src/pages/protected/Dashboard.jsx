import { useQuery } from "@tanstack/react-query";
import { useNavigate } from "react-router";

import { dashboardOverview } from "@/api";
import Container from "@/components/Container";
import Loader from "@/components/Loader";
import EmptyDashboard from "@/components/Pages/Dashboard/Empty";
import IncidentChart from "@/components/Pages/Dashboard/IncidentChart";
import Metrics from "@/components/Pages/Dashboard/Metrics";
import RecentIncidents from "@/components/Pages/Dashboard/RecentIncidents";
import QueryError from "@/components/QueryError";
import QueryPageHeader from "@/components/QueryPageHeader";
import authenticatedClient from "@/core/api/customClient";
import isEmptyData from "@/shared/utils/isEmptyData";

function DashboardPage() {
	const navigate = useNavigate();

	const { data, isPending, isError, isFetching, refetch } = useQuery({
		queryKey: ["dashboard-overview"],
		queryFn: () =>
			dashboardOverview({
				client: authenticatedClient,
			}),
		select: (response) => response.data,
	});

	if (isPending) {
		return <Loader />;
	}

	if (isError) {
		return <QueryError onRetry={refetch} />;
	}

	if (isEmptyData(data)) {
		return (
			<EmptyDashboard
				onAction={() => {
					navigate("create-source-app");
				}}
			/>
		);
	}

	return (
		<Container className="space-y-8">
			<QueryPageHeader
				title="Dashboard"
				description="View application metrics, incident trends, and recent security events."
				onRefresh={refetch}
				isRefreshing={isFetching}
			/>
			<Metrics data={data} />
			<IncidentChart incidents={data.daily_incidents_over_last_30_days} />
			<RecentIncidents incidents={data.last_5_incidents} />
		</Container>
	);
}

export default DashboardPage;
