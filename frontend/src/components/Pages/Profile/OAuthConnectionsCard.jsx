import { useQuery } from "@tanstack/react-query";
import { CheckCircle2, CircleAlert, Link2, LoaderCircle, ShieldCheck } from "lucide-react";

import { getOauthConnections } from "@/api";
import GoogleProfileSignIn from "@/components/Google/GoogleProfileSignIn";
import authenticatedClient from "@/core/api/customClient";

function OAuthConnectionsCard() {
	const { data, isPending, isError, error, isFetching, refetch } = useQuery({
		queryKey: ["oauthConnections"],
		queryFn: () =>
			getOauthConnections({
				client: authenticatedClient,
			}),
	});

	const googleEnabled =
		data?.data?.connections?.some(
			(connection) => connection.provider.toLowerCase() === "google",
		) ?? false;

	return (
		<section className="bg-surface border-border w-full min-w-0 overflow-hidden rounded-2xl border shadow-sm">
			{/* Header */}
			<div className="flex items-start gap-4 p-5 sm:p-6">
				<div className="bg-primary/10 text-primary flex size-11 shrink-0 items-center justify-center rounded-xl">
					<ShieldCheck className="size-5" aria-hidden="true" />
				</div>

				<div className="min-w-0 flex-1">
					<h2 className="text-t-primary text-base font-semibold">Connected accounts</h2>
					<p className="text-t-secondary mt-1 text-sm leading-relaxed">
						Manage the accounts connected to your profile and the services you can use
						to sign in.
					</p>
				</div>
			</div>

			<div className="border-border border-t" />

			{/* Google connection */}
			<div className="flex flex-col gap-4 p-5 sm:flex-row sm:items-center sm:justify-between sm:p-6">
				<div className="flex min-w-0 items-center gap-3">
					<div className="border-border bg-surface-secondary flex size-11 shrink-0 items-center justify-center rounded-xl border">
						<Link2 className="text-t-primary size-5" aria-hidden="true" />
					</div>

					<div className="min-w-0">
						<div className="flex flex-wrap items-center gap-2">
							<p className="text-t-primary font-medium">Google</p>

							{!isPending && !isError && (
								<span
									className={`inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-xs font-medium ${
										googleEnabled
											? "bg-green-500/10 text-green-600"
											: "bg-surface-secondary text-t-secondary"
									}`}
								>
									{googleEnabled ? (
										<>
											<CheckCircle2 className="size-3.5" />
											Connected
										</>
									) : (
										"Not connected"
									)}
								</span>
							)}
						</div>

						<p className="text-t-secondary mt-1 text-sm">
							{isPending
								? "Checking your connection…"
								: isError
									? "Unable to check connection status."
									: googleEnabled
										? "Your Google account is linked and ready to use."
										: "Link your Google account to enable Google sign-in."}
						</p>
					</div>
				</div>

				<div className="flex shrink-0 items-center sm:justify-end">
					{isPending ? (
						<div className="text-t-secondary inline-flex items-center gap-2 text-sm">
							<LoaderCircle className="size-4 animate-spin" aria-hidden="true" />
							Loading
						</div>
					) : isError ? (
						<button
							type="button"
							className="border-border text-t-primary hover:bg-surface-secondary inline-flex min-h-10 items-center justify-center gap-2 rounded-lg border px-4 py-2 text-sm font-medium transition-colors"
							onClick={() => void refetch()}
							disabled={isFetching}
						>
							{isFetching && <LoaderCircle className="size-4 animate-spin" />}
							Try again
						</button>
					) : googleEnabled ? (
						<div className="inline-flex items-center gap-2 text-sm font-medium text-green-600">
							<CheckCircle2 className="size-4" aria-hidden="true" />
							Active
						</div>
					) : (
						<GoogleProfileSignIn
							isActive
							onSuccess={() => {
								// The GoogleProfileSignIn mutation invalidates
								// ["oauthConnections"], so this query refreshes.
							}}
						/>
					)}
				</div>
			</div>

			{/* Query error */}
			{isError && (
				<div
					role="alert"
					className="border-t border-red-500/20 bg-red-500/5 px-5 py-3 sm:px-6"
				>
					<div className="flex items-start gap-2">
						<CircleAlert
							className="mt-0.5 size-4 shrink-0 text-red-600"
							aria-hidden="true"
						/>
						<div className="text-sm">
							<p className="font-medium text-red-600">
								Could not load connected accounts
							</p>
							<p className="text-t-secondary mt-1">
								{error instanceof Error
									? error.message
									: "Please check your connection and try again."}
							</p>
						</div>
					</div>
				</div>
			)}
		</section>
	);
}

export default OAuthConnectionsCard;
