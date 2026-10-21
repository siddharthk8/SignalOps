import { useCallback, useEffect, useRef, useState } from "react";

import useTheme from "@/shared/hooks/useTheme";
import { initializeGoogle, setGoogleCallback } from "@/shared/services/googleIdentity";

export default function GoogleAuthButton({ onCredential, disabled = false }) {
	const buttonRef = useRef(null);
	const callbackRef = useRef(onCredential);
	const { theme, systemTheme } = useTheme();
	const [scriptReady, setScriptReady] = useState(false);

	// Keep the latest parent callback.
	useEffect(() => {
		callbackRef.current = onCredential;
	}, [onCredential]);

	// Google supports "outline" and "filled_black" button themes.
	const googleButtonTheme =
		(theme === "system" ? systemTheme : theme) === "dark" ? "filled_black" : "outline";

	// Receive the credential from Google.
	const handleGoogleResponse = useCallback((response) => {
		if (!response?.credential) {
			console.error("[GoogleAuthButton] Google did not return a credential");
			return;
		}

		callbackRef.current?.(response.credential);
	}, []);

	// Initialize Google after its script is available.
	useEffect(() => {
		let cancelled = false;
		let script = null;
		let unregisterCallback = null;

		const initialize = () => {
			if (cancelled) return;

			if (!initializeGoogle(handleGoogleResponse)) {
				return;
			}

			unregisterCallback = setGoogleCallback(handleGoogleResponse);
			setScriptReady(true);
		};

		if (window.google?.accounts?.id) {
			initialize();
		} else {
			script = document.querySelector('script[src="https://accounts.google.com/gsi/client"]');
			script?.addEventListener("load", initialize);
		}

		return () => {
			cancelled = true;
			script?.removeEventListener("load", initialize);
			unregisterCallback?.();
		};
	}, [handleGoogleResponse]);

	// Render or update the button when the theme changes.
	useEffect(() => {
		if (!scriptReady || !buttonRef.current || !window.google?.accounts?.id) {
			return;
		}

		const container = buttonRef.current;
		container.replaceChildren();

		window.google.accounts.id.renderButton(container, {
			theme: googleButtonTheme,
			size: "large",
			text: "continue_with",
			shape: "pill",
			width: Math.min(260, container.clientWidth || 260),
			type: "standard",
			logo_alignment: "left",
		});
	}, [scriptReady, googleButtonTheme]);

	return (
		<div
			ref={buttonRef}
			className={`flex h-10 min-h-10 w-full min-w-0 items-center justify-center ${
				disabled ? "pointer-events-none opacity-40" : ""
			}`}
			aria-disabled={disabled}
		/>
	);
}
