import { FileText } from "lucide-react";

import Collapsible from "@/components/Collapsible";
import ExpandableList from "@/components/ExpandableList";

function LogRow({ log }) {
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
		<Collapsible
			className="hover:bg-muted/20 border-border border-t transition-colors"
			header={
				<div className="min-w-0">
					<div className="mb-2 flex flex-wrap items-center gap-2">
						<span className="text-info/70 font-medium">#{log.id}</span>

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
			}
		>
			<div className="space-y-4">
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
		</Collapsible>
	);
}

function LogsCard({ logs }) {
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

			<ExpandableList
				items={logs}
				limit={5}
				className="divide-border divide-y"
				renderItem={(log) => <LogRow key={log.id} log={log} />}
			/>
		</section>
	);
}

export default LogsCard;
