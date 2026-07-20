import { useMutation, useQueryClient } from "@tanstack/react-query";
import axios from "axios";
import { Code2, Info, Send, Terminal, Upload } from "lucide-react";
import { useMemo } from "react";
import { useForm } from "react-hook-form";
import { useNavigate, useParams } from "react-router";

import { ingestLogs } from "@/api";
import Button from "@/components/Button";
import Container from "@/components/Container";
import FormMessage from "@/components/Form/FormMessage";
import authenticatedClient from "@/core/api/customClient";
import { SERVER_ERROR_MSG } from "@/shared/constants/messages";

const SAMPLE_PAYLOAD = (sourceAppId) => ({
	source_app_id: Number(sourceAppId),
	logs: [
		"[2026-07-19T18:45:06Z] INFO: User john.doe logged in from 192.168.1.20",
		{
			level: "error",
			message: "Payment failed for order ORD-10231. user=john.doe amount=249.99",
			timestamp: "2026-07-19T18:45:06.444865+00:00",
		},
	],
});

export default function IngestLogsPage() {
	const navigate = useNavigate();
	const { sourceAppId } = useParams();

	const defaultJson = useMemo(
		() => JSON.stringify(SAMPLE_PAYLOAD(sourceAppId), null, 2),
		[sourceAppId],
	);

	const {
		register,
		handleSubmit,
		setError,
		clearErrors,
		formState: { errors, isSubmitting },
	} = useForm({
		mode: "onBlur",
		defaultValues: {
			payload: defaultJson,
		},
	});

	const queryClient = useQueryClient();

	const { mutate } = useMutation({
		mutationFn: (body) =>
			ingestLogs({
				client: authenticatedClient,
				body,
			}),

		onSuccess: () => {
			queryClient.invalidateQueries({
				queryKey: ["batches", sourceAppId],
			});
			navigate(-1);
		},

		onError: (error) => {
			if (!axios.isAxiosError(error)) {
				setError("root", {
					type: "server",
					message: SERVER_ERROR_MSG,
				});
				return;
			}

			setError("root", {
				type: "server",
				message: error.response?.data?.message || error.message || SERVER_ERROR_MSG,
			});
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
				{/* Header */}

				<div className="flex items-start justify-between">
					<div>
						<div className="mb-2 flex items-center gap-3">
							<div className="bg-primary/10 text-primary flex h-11 w-11 items-center justify-center rounded-md">
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

				{/* Recommendation */}
				<div className="border-primary/20 bg-primary/5 rounded-md border p-5">
					<div className="flex items-start gap-4">
						<div className="bg-primary/10 text-primary flex h-10 w-10 shrink-0 items-center justify-center rounded-md">
							<Info size={18} />
						</div>

						<div className="space-y-2">
							<h2 className="font-semibold">Recommended for development only</h2>

							<p className="text-t-muted text-sm leading-6">
								This playground exists for quickly testing log ingestion using raw
								JSON payloads.
							</p>

							<div className="bg-surface border-border rounded-md border p-3">
								<div className="mb-1 flex items-center gap-2 text-sm font-medium">
									<Terminal size={15} className="text-primary" />
									Production Recommendation
								</div>

								<p className="text-t-muted text-sm">
									Applications should send logs directly to
									<span className="bg-muted mx-1 rounded px-2 py-1 font-mono text-xs">
										POST /api/v1/logs
									</span>
									using the ingestion API instead of this UI.
								</p>
							</div>
						</div>
					</div>
				</div>

				<FormMessage message={errors.root?.message} />

				<form
					onSubmit={handleSubmit(onSubmit)}
					className="border-border bg-surface overflow-hidden rounded-md border"
					noValidate
				>
					<div className="border-border flex items-center justify-between border-b px-6 py-4">
						<div>
							<h2 className="text-lg font-semibold">JSON Payload</h2>

							<p className="text-t-muted mt-1 text-sm">
								Paste a payload matching the ingestion schema.
							</p>
						</div>

						<div className="bg-primary/10 text-primary flex h-10 w-10 items-center justify-center rounded-md">
							<Code2 size={18} />
						</div>
					</div>

					<div className="p-6">
						<textarea
							{...register("payload", {
								required: "Payload is required.",
							})}
							spellCheck={false}
							className="border-border bg-muted/20 focus:border-primary focus:ring-primary/20 min-h-[520px] w-full rounded-md border p-5 font-mono text-[13px] leading-7 transition outline-none focus:ring-2"
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
								disabled={isSubmitting}
								rightIcon={<Send size={16} />}
								className="min-w-40"
							>
								{isSubmitting ? "Ingesting..." : "Ingest Logs"}
							</Button>
						</div>
					</div>
				</form>
			</div>
		</Container>
	);
}
