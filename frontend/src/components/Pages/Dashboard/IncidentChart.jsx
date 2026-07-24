import { useMemo } from "react";
import {
	Area,
	AreaChart,
	CartesianGrid,
	ResponsiveContainer,
	Tooltip,
	XAxis,
	YAxis,
} from "recharts";

function CustomTooltip({ active, payload, label }) {
	if (!active || !payload?.length) {
		return null;
	}

	return (
		<div className="border-border bg-surface rounded-md border px-3 py-2 shadow-lg">
			<p className="text-t-muted text-xs">{label}</p>

			<p className="text-t-primary mt-1 text-sm font-semibold">
				{Number(payload[0].value).toLocaleString()} incidents
			</p>
		</div>
	);
}

function IncidentChart({ incidents }) {
	const chartData = useMemo(
		() =>
			incidents.map(({ date, count }) => ({
				date: new Date(date).toLocaleDateString("en-US", {
					month: "short",
					day: "numeric",
				}),
				incidents: count,
			})),
		[incidents],
	);

	const averagePerDay = useMemo(() => {
		if (!incidents.length) return 0;

		const total = incidents.reduce((sum, item) => sum + item.count, 0);
		const start = new Date(incidents[0].date);
		const end = new Date(incidents[incidents.length - 1].date);

		const days = (end - start) / (1000 * 60 * 60 * 24) + 1;
		return (total / days).toFixed(1);
	}, [incidents]);

	return (
		<section className="border-border bg-surface overflow-hidden rounded-lg border">
			<div className="border-border flex items-start justify-between border-b px-6 py-5">
				<div>
					<h2 className="text-t-primary text-lg font-semibold">Incident Trend</h2>

					<p className="text-t-muted mt-1 text-sm">
						Daily incident volume over the last 30 days.
					</p>
				</div>

				<div className="text-right">
					<p className="text-t-muted text-xs tracking-wide uppercase">Average</p>

					<p className="text-t-primary text-xl font-bold">{averagePerDay}/day</p>
				</div>
			</div>

			<div className="h-[340px] p-5">
				{chartData.length === 0 ? (
					<div className="text-t-muted flex h-full items-center justify-center text-sm">
						No incident data available.
					</div>
				) : (
					<ResponsiveContainer width="100%" height="100%">
						<AreaChart
							data={chartData}
							margin={{
								top: 10,
								right: 10,
								left: -20,
								bottom: 0,
							}}
						>
							<defs>
								<linearGradient id="incidentGradient" x1="0" y1="0" x2="0" y2="1">
									<stop offset="5%" stopColor="currentColor" stopOpacity={0.18} />

									<stop offset="100%" stopColor="currentColor" stopOpacity={0} />
								</linearGradient>
							</defs>

							<CartesianGrid
								vertical={false}
								strokeDasharray="3 3"
								className="stroke-border"
							/>

							<XAxis
								dataKey="date"
								axisLine={false}
								tickLine={false}
								tick={{ fontSize: 12 }}
							/>

							<YAxis
								allowDecimals={false}
								axisLine={false}
								tickLine={false}
								width={35}
								tick={{ fontSize: 12 }}
							/>

							<Tooltip content={<CustomTooltip />} />

							<Area
								type="monotone"
								dataKey="incidents"
								className="text-primary"
								stroke="currentColor"
								strokeWidth={2.5}
								fill="url(#incidentGradient)"
								activeDot={{
									r: 4,
									strokeWidth: 2,
								}}
							/>
						</AreaChart>
					</ResponsiveContainer>
				)}
			</div>
		</section>
	);
}

export default IncidentChart;
