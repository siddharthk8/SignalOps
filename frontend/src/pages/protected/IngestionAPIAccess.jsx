import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import axios from "axios";
import {
	AlertTriangle,
	Check,
	ChevronDown,
	ChevronUp,
	Code2,
	Copy,
	KeyRound,
	LockKeyhole,
	RefreshCw,
	ShieldCheck,
	Terminal,
	Trash2,
} from "lucide-react";
import { useState } from "react";
import { useParams } from "react-router";

import { deleteSourceAppAccessToken, generateSourceAppAccessToken, getSourceApp } from "@/api";
import Button from "@/components/Button";
import Container from "@/components/Container";
import authenticatedClient from "@/core/api/customClient";
import config from "@/core/config";
import { SERVER_ERROR_MSG } from "@/shared/constants/messages";

const API_BASE_URL = `${config.apiUrl}/api/v1`;
const LOGS_ENDPOINT = `${API_BASE_URL}/logs`;

export default function ApiAccessPage() {
	const { sourceAppId } = useParams();
	const queryClient = useQueryClient();

	const parsedSourceAppId = Number(sourceAppId);

	const [newToken, setNewToken] = useState("");
	const [showSecret, setShowSecret] = useState(true);
	const [showRevokeConfirm, setShowRevokeConfirm] = useState(false);
	const [copied, setCopied] = useState("");
	const [language, setLanguage] = useState("curl");
	const [error, setError] = useState("");
	const [success, setSuccess] = useState("");

	const {
		data: sourceAppResponse,
		isLoading: isLoadingSourceApp,
		isError: isSourceAppError,
		error: sourceAppError,
	} = useQuery({
		queryKey: ["sourceApp", parsedSourceAppId],
		queryFn: () =>
			getSourceApp({
				client: authenticatedClient,
				path: {
					source_app_id: parsedSourceAppId,
				},
			}),
		enabled: Number.isInteger(parsedSourceAppId) && parsedSourceAppId > 0,
	});

	// Supports either a direct object or an Axios-style { data } response.
	const sourceApp = sourceAppResponse?.data ?? sourceAppResponse;
	const accessKey = sourceApp?.access_key;
	const token = Boolean(sourceApp?.has_access_token);

	const getErrorMessage = (err) => {
		if (!axios.isAxiosError(err)) {
			return SERVER_ERROR_MSG;
		}

		return err.response?.data?.message || SERVER_ERROR_MSG;
	};

	const refreshSourceApp = () =>
		queryClient.invalidateQueries({
			queryKey: ["sourceApp", parsedSourceAppId],
		});

	const { mutate: generateToken, isPending: isGenerating } = useMutation({
		mutationFn: () =>
			generateSourceAppAccessToken({
				client: authenticatedClient,
				body: {
					source_app_id: parsedSourceAppId,
				},
			}),

		onSuccess: async (response) => {
			const generatedToken = response?.access_token ?? response?.data?.access_token;

			if (!generatedToken) {
				setError("Unable to retrieve the generated token. Check the API response format.");
				setSuccess("");
				await refreshSourceApp();
				return;
			}

			setNewToken(generatedToken);
			setShowSecret(true);
			setShowRevokeConfirm(false);
			setError("");
			setSuccess("Access token generated successfully.");

			await refreshSourceApp();
		},

		onError: (err) => {
			setError(getErrorMessage(err));
			setSuccess("");
		},
	});

	const { mutate: revokeToken, isPending: isRevoking } = useMutation({
		mutationFn: () =>
			deleteSourceAppAccessToken({
				client: authenticatedClient,
				body: {
					source_app_id: parsedSourceAppId,
				},
			}),

		onSuccess: async () => {
			setNewToken("");
			setShowSecret(true);
			setShowRevokeConfirm(false);
			setError("");
			setSuccess("Access token revoked successfully.");

			await refreshSourceApp();
		},

		onError: (err) => {
			setError(getErrorMessage(err));
			setSuccess("");
		},
	});

	const handleGenerateOrRotate = () => {
		setError("");
		setSuccess("");
		generateToken();
	};

	const handleRevoke = () => {
		setError("");
		setSuccess("");
		revokeToken();
	};

	const samplePayload = {
		source_app_id: parsedSourceAppId,
		logs: [
			"FORMAT-1: Testing log",
			{
				level: "info",
				message: "Testing Log",
				timestamp: "2026-10-20T04:42:57.321891+00:00",
			},
		],
	};

	const curlExample = `curl -X POST '${LOGS_ENDPOINT}' \\
  -H 'accept: */*' \\
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' \\
  -H 'Content-Type: application/json' \\
  -d '${JSON.stringify(samplePayload, null, 2).replace(/\\/g, "\\\\").replace(/'/g, "'\\''")}'`;

	const axiosExample = `import axios from "axios";

const response = await axios.post(
  "${LOGS_ENDPOINT}",
  ${JSON.stringify(samplePayload, null, 2).replace(/^/gm, "  ")},
  {
    headers: {
      Authorization: \`Bearer \${process.env.LOG_INGESTION_TOKEN}\`,
      "Content-Type": "application/json",
      Accept: "*/*",
    },
  }
);

console.log(response.data);`;

	const code = language === "curl" ? curlExample : axiosExample;

	const copyText = async (value, key) => {
		try {
			await navigator.clipboard.writeText(value);
			setCopied(key);
			window.setTimeout(() => setCopied(""), 2000);
		} catch {
			setError("Unable to copy. Please copy the text manually.");
		}
	};

	if (!Number.isInteger(parsedSourceAppId) || parsedSourceAppId <= 0) {
		return (
			<Container>
				<div className="text-error py-12 text-center">
					<p className="font-semibold">Invalid source application ID</p>
					<p className="text-t-muted mt-2 text-sm">Check the URL and try again.</p>
				</div>
			</Container>
		);
	}

	if (isLoadingSourceApp) {
		return (
			<Container>
				<div className="text-t-muted py-12 text-center text-sm">
					Loading source application...
				</div>
			</Container>
		);
	}

	if (isSourceAppError || !sourceApp) {
		return (
			<Container>
				<div className="py-12 text-center">
					<p className="text-error font-semibold">Unable to load source application</p>
					<p className="text-t-muted mt-2 text-sm">
						{sourceAppError?.response?.data?.message ??
							sourceAppError?.message ??
							SERVER_ERROR_MSG}
					</p>
				</div>
			</Container>
		);
	}

	return (
		<Container>
			<div className="mx-auto max-w-6xl space-y-8 py-4">
				{/* Page heading */}
				<div className="space-y-3">
					<div className="bg-primary/10 text-primary flex h-12 w-12 items-center justify-center rounded-xl">
						<KeyRound size={24} />
					</div>

					<div>
						<p className="text-t-muted mb-2 text-sm font-medium">
							Developer tools / Production
						</p>

						<h1 className="font-['Space_Grotesk'] text-3xl font-bold tracking-tight">
							API Access
						</h1>

						<p className="text-t-muted mt-2 max-w-2xl text-sm leading-6">
							Manage the credentials your application uses to submit logs through the
							ingestion API.
						</p>

						<p className="text-t-muted mt-2 text-sm">
							Source application:{" "}
							<span className="text-t-primary font-medium">{sourceApp.name}</span>
						</p>
					</div>
				</div>

				{/* Security notice */}
				<div className="border-border bg-muted/20 flex items-start gap-3 rounded-lg border p-4">
					<ShieldCheck className="text-primary mt-0.5 shrink-0" size={20} />

					<div>
						<p className="text-sm font-semibold">Keep your access token secure</p>

						<p className="text-t-muted mt-1 text-sm leading-6">
							Store it in your server-side environment variables or secret manager.
							Never expose production tokens in browser code, public repositories, or
							client-side logs.
						</p>
					</div>
				</div>

				{/* Error message */}
				{error && (
					<div
						role="alert"
						className="border-error/30 bg-error/5 text-error flex items-start gap-2 rounded-lg border p-4 text-sm"
					>
						<AlertTriangle size={18} className="mt-0.5 shrink-0" />
						<div className="flex-1">{error}</div>
						<button type="button" onClick={() => setError("")} className="underline">
							Dismiss
						</button>
					</div>
				)}

				{/* Success message */}
				{success && (
					<div
						role="status"
						className="border-success/30 bg-success/5 text-success flex items-center gap-2 rounded-lg border p-4 text-sm"
					>
						<Check size={18} />
						<span className="flex-1">{success}</span>
						<button type="button" onClick={() => setSuccess("")} className="underline">
							Dismiss
						</button>
					</div>
				)}

				{/* Token management */}
				<section className="border-border bg-surface overflow-hidden rounded-xl border shadow-sm">
					<div className="border-border flex items-center justify-between gap-4 border-b p-5 sm:p-6">
						<div className="flex items-center gap-3">
							<div className="bg-primary/10 text-primary flex h-10 w-10 items-center justify-center rounded-lg">
								<LockKeyhole size={20} />
							</div>

							<div>
								<h2 className="font-semibold">Access token</h2>
								<p className="text-t-muted mt-1 text-sm">
									Used to authenticate log ingestion requests.
								</p>
							</div>
						</div>

						<span
							className={`rounded-full px-3 py-1 text-xs font-medium ${
								token ? "bg-success/10 text-success" : "bg-muted text-t-muted"
							}`}
						>
							{token ? "Configured" : "Not configured"}
						</span>
					</div>

					<div className="space-y-5 p-5 sm:p-6">
						{/* Newly generated token */}
						{newToken && (
							<div className="border-success/30 bg-success/5 rounded-lg border p-4">
								<div className="flex items-start gap-3">
									<ShieldCheck
										size={20}
										className="text-success mt-0.5 shrink-0"
									/>

									<div className="min-w-0 flex-1">
										<p className="text-sm font-semibold">
											Your new access token
										</p>

										<p className="text-t-muted mt-1 text-sm">
											Copy and securely save this secret. For security
											reasons, it will not be displayed again after you leave
											this page.
										</p>

										<div className="border-border bg-surface mt-4 flex items-center gap-2 rounded-lg border p-3">
											<code className="min-w-0 flex-1 text-xs break-all">
												{showSecret ? newToken : "•".repeat(24)}
											</code>

											<button
												type="button"
												title={showSecret ? "Hide token" : "Show token"}
												onClick={() => setShowSecret(!showSecret)}
												className="text-t-muted hover:text-t-primary shrink-0"
											>
												{showSecret ? (
													<ChevronUp size={18} />
												) : (
													<ChevronDown size={18} />
												)}
											</button>

											<button
												type="button"
												title="Copy token"
												onClick={() => copyText(newToken, "token")}
												className="text-t-muted hover:text-t-primary shrink-0"
											>
												{copied === "token" ? (
													<Check size={18} />
												) : (
													<Copy size={18} />
												)}
											</button>
										</div>

										<button
											type="button"
											onClick={() => {
												setNewToken("");
												setShowSecret(true);
											}}
											className="text-t-muted mt-3 text-xs underline"
										>
											I have saved my token
										</button>
									</div>
								</div>
							</div>
						)}

						{/* Empty state */}
						{!token && !newToken && (
							<div className="border-border bg-muted/20 rounded-lg border border-dashed p-6 text-center">
								<KeyRound size={28} className="text-t-muted mx-auto mb-3" />
								<p className="font-medium">No access token configured</p>
								<p className="text-t-muted mt-1 text-sm">
									Generate a token to start authenticating log ingestion requests.
								</p>
							</div>
						)}

						{/* Existing token state */}
						{token && !newToken && (
							<div className="border-border flex items-start gap-3 rounded-lg border p-4">
								<ShieldCheck size={20} className="text-success mt-0.5 shrink-0" />
								<div>
									<p className="text-sm font-medium">
										Access token is configured ({accessKey})
									</p>
									<p className="text-t-muted mt-1 text-sm">
										The existing secret is not available to display. Rotate it
										if you need a replacement.
									</p>
								</div>
							</div>
						)}

						<div className="border-border flex flex-col gap-3 border-t pt-5 sm:flex-row sm:items-center sm:justify-between">
							<div>
								<p className="text-sm font-medium">
									{token ? "Replace access token" : "Create access token"}
								</p>
								<p className="text-t-muted mt-1 text-xs">
									{token
										? "Rotation may invalidate the previous token."
										: "Generate a credential for your server-side integration."}
								</p>
							</div>

							<div className="flex flex-wrap gap-2">
								{token && (
									<Button
										type="button"
										variant="outline"
										disabled={isGenerating || isRevoking}
										leftIcon={<Trash2 size={16} />}
										onClick={() => setShowRevokeConfirm(true)}
									>
										Revoke
									</Button>
								)}

								<Button
									type="button"
									loading={isGenerating}
									disabled={isGenerating || isRevoking}
									onClick={handleGenerateOrRotate}
									rightIcon={<RefreshCw size={16} />}
								>
									{isGenerating
										? "Generating..."
										: token
											? "Rotate token"
											: "Generate token"}
								</Button>
							</div>
						</div>
					</div>
				</section>

				{/* Integration guide */}
				<section className="border-border bg-surface overflow-hidden rounded-xl border shadow-sm">
					<div className="border-border flex items-center gap-3 border-b p-5 sm:p-6">
						<div className="bg-accent/10 text-accent flex h-10 w-10 items-center justify-center rounded-lg">
							<Terminal size={20} />
						</div>
						<div>
							<h2 className="font-semibold">Integration guide</h2>
							<p className="text-t-muted mt-1 text-sm">
								Send logs from your backend using a standard HTTP request.
							</p>
						</div>
					</div>

					<div className="space-y-5 p-5 sm:p-6">
						{/* Endpoint */}
						<div>
							<label className="text-t-muted mb-2 block text-xs font-semibold tracking-wide uppercase">
								Endpoint
							</label>

							<div className="border-border bg-muted/20 flex flex-col gap-2 rounded-lg border p-3 sm:flex-row sm:items-center">
								<span className="bg-success/10 text-success w-fit rounded px-2 py-1 font-mono text-xs font-bold">
									POST
								</span>
								<code className="min-w-0 flex-1 text-sm break-all">
									{LOGS_ENDPOINT}
								</code>
								<button
									type="button"
									onClick={() => copyText(LOGS_ENDPOINT, "endpoint")}
									className="text-t-muted hover:text-t-primary flex items-center gap-2 self-start text-xs sm:self-center"
								>
									{copied === "endpoint" ? (
										<Check size={15} />
									) : (
										<Copy size={15} />
									)}
									Copy
								</button>
							</div>
						</div>

						{/* Code examples */}
						<div>
							<div className="mb-3 flex flex-wrap items-center justify-between gap-3">
								<div>
									<h3 className="text-sm font-semibold">Example request</h3>
									<p className="text-t-muted mt-1 text-xs">
										Use the example that matches your environment.
									</p>
								</div>

								<div className="bg-muted flex rounded-lg p-1">
									<button
										type="button"
										onClick={() => setLanguage("curl")}
										className={`rounded-md px-3 py-1.5 text-xs font-medium ${
											language === "curl"
												? "bg-surface text-t-primary shadow-sm"
												: "text-t-muted"
										}`}
									>
										cURL
									</button>
									<button
										type="button"
										onClick={() => setLanguage("axios")}
										className={`rounded-md px-3 py-1.5 text-xs font-medium ${
											language === "axios"
												? "bg-surface text-t-primary shadow-sm"
												: "text-t-muted"
										}`}
									>
										Axios
									</button>
								</div>
							</div>

							<div className="border-border overflow-hidden rounded-lg border">
								<div className="bg-muted/30 border-border flex items-center justify-between border-b px-4 py-3">
									<div className="text-t-muted flex items-center gap-2 text-xs">
										<Code2 size={15} />
										{language === "curl" ? "Shell" : "JavaScript"}
									</div>
									<button
										type="button"
										onClick={() => copyText(code, "code")}
										className="text-t-muted hover:text-t-primary flex items-center gap-2 text-xs"
									>
										{copied === "code" ? (
											<Check size={15} />
										) : (
											<Copy size={15} />
										)}
										{copied === "code" ? "Copied" : "Copy code"}
									</button>
								</div>

								<pre className="bg-muted/10 max-h-[520px] overflow-auto p-4 text-xs leading-6">
									<code>{code}</code>
								</pre>
							</div>
						</div>

						{/* Payload information */}
						<div className="border-border rounded-lg border p-4">
							<h3 className="text-sm font-semibold">Request payload</h3>
							<p className="text-t-muted mt-1 text-sm">
								Each request includes the source application ID and an array of
								logs. Entries can be strings or structured log objects.
							</p>
						</div>
					</div>
				</section>

				{/* Revoke confirmation */}
				{showRevokeConfirm && (
					<div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
						<div
							role="alertdialog"
							aria-modal="true"
							aria-labelledby="revoke-title"
							aria-describedby="revoke-description"
							className="border-border bg-surface w-full max-w-md rounded-xl border p-6 shadow-lg"
						>
							<div className="bg-error/10 text-error mb-4 flex h-11 w-11 items-center justify-center rounded-lg">
								<AlertTriangle size={21} />
							</div>

							<h2 id="revoke-title" className="text-lg font-semibold">
								Revoke access token?
							</h2>

							<p
								id="revoke-description"
								className="text-t-muted mt-2 text-sm leading-6"
							>
								Applications using this token may no longer be able to submit logs.
								Are you sure you want to revoke this credential?
							</p>

							<div className="mt-6 flex justify-end gap-3">
								<Button
									type="button"
									variant="outline"
									disabled={isRevoking}
									onClick={() => setShowRevokeConfirm(false)}
								>
									Cancel
								</Button>
								<Button
									type="button"
									loading={isRevoking}
									disabled={isRevoking || isGenerating}
									onClick={handleRevoke}
								>
									Revoke token
								</Button>
							</div>
						</div>
					</div>
				)}
			</div>
		</Container>
	);
}
