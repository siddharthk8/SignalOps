import { useMutation, useQueryClient } from "@tanstack/react-query";
import axios from "axios";
import { useCallback, useState } from "react";

import { linkGoogleAccount } from "@/api";
import FormMessage from "@/components/Form/FormMessage";
import authenticatedClient from "@/core/api/customClient";
import { SERVER_ERROR_MSG } from "@/shared/constants/messages";

import GoogleAuthButton from "./GoogleAuthButton";

export default function GoogleProfileSignIn({ isActive = true, onSuccess }) {
	const queryClient = useQueryClient();
	const [error, setError] = useState("");

	const { mutate: enableGoogle, isPending } = useMutation({
		mutationFn: (credential) =>
			linkGoogleAccount({
				client: authenticatedClient,
				body: { credential },
			}),

		onSuccess: async (data) => {
			await queryClient.invalidateQueries({
				queryKey: ["oauthConnections"],
			});

			onSuccess?.(data);
		},

		onError: (err) => {
			setError(
				axios.isAxiosError(err)
					? err.response?.data?.message || SERVER_ERROR_MSG
					: SERVER_ERROR_MSG,
			);
		},
	});

	const handleCredential = useCallback(
		(credential) => {
			if (!isActive || isPending) return;

			setError("");
			enableGoogle(credential);
		},
		[isActive, isPending, enableGoogle],
	);

	return (
		<div className="w-full min-w-0 space-y-4">
			{error && (
				<div className="w-full min-w-0" role="alert" aria-live="polite">
					<FormMessage message={error} />
				</div>
			)}

			<div className="relative w-full min-w-0" aria-busy={isPending}>
				<GoogleAuthButton
					onCredential={handleCredential}
					disabled={!isActive || isPending}
				/>

				{isPending && (
					<div className="bg-surface/80 text-t-primary absolute inset-0 z-10 flex items-center justify-center gap-2 rounded-md text-sm">
						<span className="border-border border-t-primary size-4 animate-spin rounded-full border-2" />
						<span>Linking Google account…</span>
					</div>
				)}
			</div>
		</div>
	);
}
