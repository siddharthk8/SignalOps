import { useQuery } from "@tanstack/react-query";
import { AlertTriangle, Database, ShieldAlert } from "lucide-react";
import {
	Area,
	AreaChart,
	CartesianGrid,
	ResponsiveContainer,
	Tooltip,
	XAxis,
	YAxis,
} from "recharts";

import { dashboardOverview } from "@/api";
import Button from "@/components/Button";
import Container from "@/components/Container/Container";
import Loader from "@/components/Loader";
import authenticatedClient from "@/core/api/customClient";

function CustomTooltip({ active, payload, label }) {
	if (!active || !payload?.length) {
		return null;
	}

	return (
		<div className="border-border bg-surface rounded-xl border p-4 shadow-lg">
			<p className="text-t-muted text-xs">{label}</p>

			<p className="text-t-primary mt-2 text-sm font-bold">
				{Number(payload[0].value).toLocaleString()} incidents
			</p>
		</div>
	);
}

function DashboardPage() {
	const {
		data: overviewData,
		isLoading,
		isError,
		refetch,
	} = useQuery({
		queryKey: ["dashboard-overview"],
		queryFn: () => {
			return dashboardOverview({
				client: authenticatedClient,
			});
		},
	});

	if (isLoading) {
		return <Loader />;
	}

	if (isError || !overviewData) {
		return (
			<Container>
				<div className="flex flex-col items-center gap-4 py-20">
					<h2 className="text-xl font-semibold">Couldn't load dashboard</h2>

					<Button
						onClick={() => refetch()}
						className="bg-primary rounded-lg px-4 py-2 text-white"
					>
						Retry
					</Button>
				</div>
			</Container>
		);
	}

	const { data } = overviewData;

	const metrics = [
		{
			title: "Source Applications",
			value: data.source_apps_count,
			icon: Database,
		},
		{
			title: "Total Incidents",
			value: data.incidents_count,
			icon: AlertTriangle,
		},
		{
			title: "Unresolved Incidents",
			value: data.unresolved_incidents_count,
			icon: ShieldAlert,
		},
	];

	const chartData = data.daily_incidents_over_last_30_days.map(({ date, count }) => ({
		date: new Date(date).toLocaleDateString("en-US", {
			month: "short",
			day: "numeric",
		}),
		incidents: count,
	}));

	return (
		<Container>
			<div className="space-y-8">
				{/* Header */}
				<section className="flex flex-col justify-between gap-6 lg:flex-row lg:items-center">
					<div>
						<h1 className="font-['Space_Grotesk'] text-3xl font-bold tracking-tight">
							Overview
						</h1>

						<p className="text-t-muted mt-2 text-sm">
							Overview of monitored applications and incidents.
						</p>
					</div>
				</section>

				{/* Metric Cards */}
				<section className="grid gap-5 sm:grid-cols-2 xl:grid-cols-3">
					{metrics.map((metric) => {
						const Icon = metric.icon;

						return (
							<div
								key={metric.title}
								className="border-border bg-surface rounded-2xl border p-5"
							>
								<div className="bg-primary-100 text-primary flex h-11 w-11 items-center justify-center rounded-xl">
									<Icon size={20} />
								</div>

								<div className="mt-5">
									<p className="text-t-muted text-sm">{metric.title}</p>

									<h2 className="mt-2 text-3xl font-bold">
										{metric.value.toLocaleString()}
									</h2>
								</div>
							</div>
						);
					})}
				</section>

				{/* Incident Trend */}
				<section className="border-border bg-surface rounded-2xl border p-6">
					<div className="mb-6">
						<h2 className="font-semibold">Incidents Over Last 30 Days</h2>

						<p className="text-t-muted text-sm">Daily incident count</p>
					</div>

					<div className="h-[350px]">
						<ResponsiveContainer width="100%" height="100%">
							<AreaChart data={chartData}>
								<CartesianGrid strokeDasharray="3 3" />

								<XAxis dataKey="date" />
								<YAxis allowDecimals={false} />
								<Tooltip content={<CustomTooltip />} />

								<Area
									type="monotone"
									dataKey="incidents"
									stroke="currentColor"
									fill="currentColor"
									className="text-primary"
								/>
							</AreaChart>
						</ResponsiveContainer>
					</div>
				</section>

				{/* Recent Incidents */}
				<section className="border-border bg-surface rounded-2xl border p-6">
					<div className="mb-6 flex items-center justify-between">
						<div>
							<h2 className="font-semibold">Recent Incidents</h2>

							<p className="text-t-muted text-sm">
								Last 5 incidents received from backend
							</p>
						</div>

						<AlertTriangle className="text-error" size={20} />
					</div>

					{data.last_5_incidents.length === 0 ? (
						<div className="text-t-muted py-10 text-center">No incidents found.</div>
					) : (
						<div className="grid gap-4 lg:grid-cols-2 xl:grid-cols-3">
							{data.last_5_incidents.map((incident, index) => (
								<div key={index} className="border-border rounded-xl border p-5">
									{/* Replace once IncidentResponse is known */}

									<p className="text-t-muted text-sm">Incident #{index + 1}</p>

									<pre className="bg-bg mt-4 overflow-auto rounded p-3 text-xs">
										{JSON.stringify(incident, null, 2)}
									</pre>
								</div>
							))}
						</div>
					)}
				</section>
			</div>
		</Container>
	);
}

export default DashboardPage;
