import { ChevronDown, ChevronUp, FileText } from "lucide-react";
import { useState } from "react";

function LogsCard({ logs }) {
	const [showAll, setShowAll] = useState(false);
	const [expandedLogs, setExpandedLogs] = useState({});

	const visibleLogs = showAll ? logs : logs.slice(0, 5);

	const toggleLog = (id) => {
		setExpandedLogs((prev) => ({
			...prev,
			[id]: !prev[id],
		}));
	};

	return (
		<section className="bg-surface border-border overflow-hidden rounded-md border">
			<div className="border-border flex items-center justify-between border-b px-5 py-4">
				<div>
					<h2 className="text-base font-semibold">Logs</h2>

					<p className="text-t-muted mt-1 text-sm">
						Original application logs received during ingestion.
					</p>
				</div>

				<div className="bg-info/10 text-info flex h-9 w-9 items-center justify-center rounded-md">
					<FileText size={18} />
				</div>
			</div>

			<div className="divide-border divide-y">
				{visibleLogs.map((log) => {
					const isExpanded = expandedLogs[log.id];

					const metadata = [
						["Level", log.level],
						["Time", log.timestamp],
						["User", log.user],
						["Email", log.email],
						["IP", log.ip_address],
						["Session", log.session_id],
						["Token", log.token_id],
						["Request", log.request_id],
					].filter(([, value]) => value);

					return (
						<div key={log.id} className="hover:bg-muted/20 px-5 py-4 transition-colors">
							<button
								onClick={() => toggleLog(log.id)}
								className="flex w-full items-center justify-between text-left"
							>
								<div className="min-w-0">
									<div className="mb-2 flex flex-wrap items-center gap-2">
										<span className="font-medium">#{log.id}</span>

										{metadata.slice(0, 4).map(([label, value]) => (
											<span
												key={label}
												className="bg-muted text-t-muted rounded px-2 py-0.5 text-[11px]"
											>
												{value}
											</span>
										))}
									</div>

									<p className="text-t-muted truncate text-sm">{log.message}</p>
								</div>

								{isExpanded ? (
									<ChevronUp size={16} className="text-t-muted ml-4 shrink-0" />
								) : (
									<ChevronDown size={16} className="text-t-muted ml-4 shrink-0" />
								)}
							</button>

							{isExpanded && (
								<div className="mt-4 space-y-4">
									{metadata.length > 0 && (
										<div className="flex flex-wrap gap-2">
											{metadata.map(([label, value]) => (
												<div
													key={label}
													className="border-border bg-muted/40 rounded-md border px-2 py-1 text-xs"
												>
													<span className="text-t-muted">{label}:</span>{" "}
													<span className="font-medium">{value}</span>
												</div>
											))}
										</div>
									)}

									<pre className="bg-muted/30 border-border overflow-x-auto rounded-md border p-3 font-mono text-[13px] leading-6 break-words whitespace-pre-wrap">
										{log.message}
									</pre>
								</div>
							)}
						</div>
					);
				})}
			</div>

			{logs.length > 5 && (
				<div className="border-border border-t px-5 py-3">
					<button
						onClick={() => setShowAll((prev) => !prev)}
						className="text-primary hover:text-primary/80 flex items-center gap-2 text-sm font-medium"
					>
						{showAll ? (
							<>
								<ChevronUp size={16} />
								Show Less
							</>
						) : (
							<>
								<ChevronDown size={16} />
								Show All ({logs.length})
							</>
						)}
					</button>
				</div>
			)}
		</section>
	);
}

export default LogsCard;
