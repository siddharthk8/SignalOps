import { useMutation } from "@tanstack/react-query";
import axios from "axios";
import { useCallback, useState } from "react";

import { googleLogin } from "@/api";
import FormMessage from "@/components/Form/FormMessage";
import { SERVER_ERROR_MSG } from "@/shared/constants/messages";

import GoogleAuthButton from "./GoogleAuthButton";

export default function AuthLoginSignup({ onLoginSuccess, isActive = true }) {
	const [error, setError] = useState("");

	const { mutate, isPending } = useMutation({
		mutationFn: (credential) =>
			googleLogin({
				body: { credential },
			}),
		onSuccess: (data) => {
			onLoginSuccess?.(data);
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
			mutate(credential);
		},
		[isActive, isPending, mutate],
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
						<span>Signing you in…</span>
					</div>
				)}
			</div>
		</div>
	);
}
