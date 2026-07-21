import { useQuery } from "@tanstack/react-query";
import { useParams } from "react-router";

import { getBatch } from "@/api";
import Container from "@/components/Container";
import Loader from "@/components/Loader";
import AIAnalysisCard from "@/components/Pages/BatchDetails/AIAnalysisCard";
import BatchHeader from "@/components/Pages/BatchDetails/BatchHeader";
import BatchOverviewCards from "@/components/Pages/BatchDetails/BatchOverviewCards";
import EntitiesCard from "@/components/Pages/BatchDetails/EntitiesCard";
import EventsCard from "@/components/Pages/BatchDetails/EventsCard";
import IncidentsCard from "@/components/Pages/BatchDetails/IncidentsCard";
import LogsCard from "@/components/Pages/BatchDetails/LogsCard";
import PipelineOverview from "@/components/Pages/BatchDetails/PipelineOverview";
import SignalsCard from "@/components/Pages/BatchDetails/SignalsCard";
import QueryError from "@/components/QueryError";
import authenticatedClient from "@/core/api/customClient";

function BatchDetailsPage() {
	const { batchId } = useParams();

	const { data, isPending, isError, refetch } = useQuery({
		queryKey: ["batch", batchId],
		queryFn: () =>
			getBatch({
				client: authenticatedClient,
				path: {
					batch_id: Number(batchId),
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

	const overview = {
		logs: data.logs.length,
		entities: data.entities.length,
		events: data.events.length,
		signals: data.signals.length,
		incidents: data.incidents.length,
		analyses: data.ai_analyses.length,
	};

	return (
		<Container className="space-y-8">
			<BatchHeader batchId={data.id} createdAt={data.created_at} />
			<BatchOverviewCards overview={overview} />
			<PipelineOverview />
			<AIAnalysisCard analyses={data.ai_analyses} />
			<IncidentsCard incidents={data.incidents} />
			<SignalsCard signals={data.signals} />
			<EventsCard events={data.events} />
			<EntitiesCard entities={data.entities} />
			<LogsCard logs={data.logs} />
		</Container>
	);
}

export default BatchDetailsPage;
