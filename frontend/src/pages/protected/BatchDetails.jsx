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

	const { data, isLoading, isError, refetch } = useQuery({
		queryKey: ["batch", batchId],

		queryFn: () =>
			getBatch({
				client: authenticatedClient,
				path: {
					batch_id: Number(batchId),
				},
			}),
	});

	if (isLoading) {
		return <Loader />;
	}

	if (isError || !data) {
		return <QueryError onRetry={refetch} />;
	}

	const batch = data.data;

	const overview = {
		logs: batch.logs.length,
		entities: batch.entities.length,
		events: batch.events.length,
		signals: batch.signals.length,
		incidents: batch.incidents.length,
		analyses: batch.ai_analyses.length,
	};

	return (
		<Container>
			<div className="space-y-8">
				<BatchHeader batchId={batch.id} createdAt={batch.created_at} />
				<BatchOverviewCards overview={overview} />
				<PipelineOverview />
				<AIAnalysisCard analyses={batch.ai_analyses} />
				<IncidentsCard incidents={batch.incidents} />
				<SignalsCard signals={batch.signals} />
				<EventsCard events={batch.events} />
				<EntitiesCard entities={batch.entities} />
				<LogsCard logs={batch.logs} />
			</div>
		</Container>
	);
}

export default BatchDetailsPage;
