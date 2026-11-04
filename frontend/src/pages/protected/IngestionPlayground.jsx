import { useMutation, useQueryClient } from "@tanstack/react-query";
import { AlertTriangle, Code2, Send, Upload } from "lucide-react";
import { useMemo } from "react";
import { useForm } from "react-hook-form";
import { useNavigate, useParams } from "react-router";

import { ingestLogs } from "@/api";
import Button from "@/components/Button";
import Container from "@/components/Container";
import FormMessage from "@/components/Form/FormMessage";
import authenticatedClient from "@/core/api/customClient";
import { handleServerErrorOnMutate } from "@/shared/utils/handleServerErrorOnMutate";

const SAMPLE_PAYLOAD = (sourceAppId) => ({
	source_app_id: Number(sourceAppId),
	logs: [
		"FORMAT-1: log message...",
		{
			message: "FORMAT-2: log message...",
			level: "info",
			timestamp: null,
			user: null,
			email: null,
			ip_address: null,
			session_id: null,
			token_id: null,
			request_id: null,
		},
	],
});

export default function IngestionPlayload() {
	const navigate = useNavigate();
	const { sourceAppId } = useParams();

	const defaultJson = useMemo(
		() => JSON.stringify(SAMPLE_PAYLOAD(sourceAppId), null, 4),
		[sourceAppId],
	);

	const {
		register,
		handleSubmit,
		setError,
		clearErrors,
		formState: { errors },
	} = useForm({
		mode: "onBlur",
		defaultValues: {
			payload: defaultJson,
		},
	});

	const queryClient = useQueryClient();

	const { mutate, isPending } = useMutation({
		mutationFn: (body) =>
			ingestLogs({
				client: authenticatedClient,
				body,
			}),
		onSuccess: () => {
			queryClient.invalidateQueries({
				queryKey: ["batches", sourceAppId],
			});
			navigate(`/source-apps/${sourceAppId}/batches`);
		},
		onError: (error) => {
			handleServerErrorOnMutate(error, setError);
		},
	});

	const onSubmit = ({ payload }) => {
		clearErrors();

		let parsed;

		try {
			parsed = JSON.parse(payload);
		} catch {
			setError("payload", {
				type: "manual",
				message: "Invalid JSON payload.",
			});
			return;
		}

		if (!Array.isArray(parsed.logs)) {
			setError("payload", {
				type: "manual",
				message: '"logs" must be an array.',
			});
			return;
		}

		parsed.source_app_id = Number(sourceAppId);
		mutate(parsed);
	};

	return (
		<Container>
			<div className="mx-auto max-w-6xl space-y-6">
				<div className="flex items-start justify-between">
					<div>
						<div className="mb-2 flex items-center gap-3">
							<div className="bg-primary/10 text-primary flex h-11 w-11 items-center justify-center rounded-lg">
								<Upload size={20} />
							</div>

							<div>
								<h1 className="font-['Space_Grotesk'] text-3xl font-bold">
									Ingest Logs
								</h1>

								<p className="text-t-muted mt-1 text-sm">
									Developer playground for testing log ingestion.
								</p>
							</div>
						</div>
					</div>
				</div>

				<FormMessage message={errors.root?.message} />

				<form
					onSubmit={handleSubmit(onSubmit)}
					className="border-border bg-surface overflow-hidden rounded-lg border"
					noValidate
				>
					<div className="border-border flex items-center justify-between border-b px-6 py-4">
						<div>
							<h2 className="text-lg font-semibold">JSON Payload</h2>

							<p className="text-t-muted mt-1 text-sm">
								Paste a payload matching the ingestion schema.
							</p>
						</div>

						<div className="bg-primary/10 text-primary flex h-10 w-10 items-center justify-center rounded-lg">
							<Code2 size={18} />
						</div>
					</div>

					<div className="p-6">
						<div className="border-warning/30 bg-warning/5 mb-4 flex items-start gap-3 rounded-lg border p-4">
							<AlertTriangle size={18} className="text-warning mt-0.5 shrink-0" />

							<div className="text-sm">
								<p className="text-warning font-semibold">Submission limits</p>

								<ul className="text-t-muted mt-2 list-inside list-disc space-y-1">
									<li>Maximum 100 logs per submission.</li>
									<li>Maximum 500 characters per log message.</li>
								</ul>

								<p className="text-t-muted mt-2 leading-5">
									The{" "}
									<code className="bg-muted rounded px-1 py-0.5 text-xs">
										logs
									</code>{" "}
									array supports plain-text messages, structured JSON log objects,
									or a combination of both.
								</p>
							</div>
						</div>

						<textarea
							{...register("payload", {
								required: "Payload is required.",
							})}
							spellCheck={false}
							className="border-border bg-muted/20 focus:border-primary focus:ring-primary/20 min-h-[520px] w-full rounded-lg border p-5 font-mono text-[13px] leading-7 transition outline-none focus:ring-2"
						/>

						{errors.payload && (
							<p className="text-error mt-2 text-sm">{errors.payload.message}</p>
						)}

						<div className="border-border mt-6 flex items-center justify-between border-t pt-6">
							<div className="text-t-muted text-sm">
								The
								<span className="bg-muted mx-1 rounded px-1.5 py-0.5 font-mono">
									source_app_id
								</span>
								is automatically replaced with the current application ID.
							</div>

							<Button
								type="submit"
								loading={isPending}
								disabled={isPending}
								rightIcon={<Send size={16} />}
								loadingText="Processing..."
							>
								Ingest Logs
							</Button>
						</div>
					</div>
				</form>
			</div>
		</Container>
	);
}
