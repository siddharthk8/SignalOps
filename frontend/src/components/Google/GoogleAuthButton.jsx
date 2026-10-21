import { useCallback, useEffect, useRef, useState } from "react";

import useTheme from "@/shared/hooks/useTheme";
import { initializeGoogle, setGoogleCallback } from "@/shared/services/googleIdentity";

const GOOGLE_SCRIPT_SRC = "https://accounts.google.com/gsi/client";

export default function GoogleAuthButton({ onCredential, disabled = false }) {
	const buttonRef = useRef(null);
	const callbackRef = useRef(onCredential);
	const renderedRef = useRef(false);

	const { theme, systemTheme } = useTheme();

	const [scriptReady, setScriptReady] = useState(
		() => typeof window !== "undefined" && Boolean(window.google?.accounts?.id),
	);
	const [buttonReady, setButtonReady] = useState(false);

	useEffect(() => {
		callbackRef.current = onCredential;
	}, [onCredential]);

	const resolvedTheme = theme === "system" ? systemTheme : theme;

	const googleButtonTheme = resolvedTheme === "dark" ? "filled_black" : "outline";

	const handleGoogleResponse = useCallback((response) => {
		if (response?.credential) {
			callbackRef.current?.(response.credential);
		}
	}, []);

	// Load the GIS script if necessary.
	useEffect(() => {
		let cancelled = false;

		const handleLoad = () => {
			if (!cancelled && window.google?.accounts?.id) {
				setScriptReady(true);
			}
		};

		if (window.google?.accounts?.id) {
			return () => {
				cancelled = true;
			};
		}

		let script = document.querySelector(`script[src="${GOOGLE_SCRIPT_SRC}"]`);

		if (!script) {
			script = document.createElement("script");
			script.src = GOOGLE_SCRIPT_SRC;
			script.async = true;
			script.defer = true;
			script.addEventListener("load", handleLoad);
			document.head.appendChild(script);
		} else {
			script.addEventListener("load", handleLoad);
			handleLoad();
		}

		return () => {
			cancelled = true;
			script?.removeEventListener("load", handleLoad);
		};
	}, []);

	// Initialize GIS and register the callback.
	useEffect(() => {
		if (!scriptReady) return;
		if (!initializeGoogle(handleGoogleResponse)) return;

		return setGoogleCallback(handleGoogleResponse);
	}, [scriptReady, handleGoogleResponse]);

	// Render once with the initial resolved theme.
	useEffect(() => {
		if (
			!scriptReady ||
			!buttonRef.current ||
			!window.google?.accounts?.id ||
			renderedRef.current
		) {
			return;
		}

		const container = buttonRef.current;

		window.google.accounts.id.renderButton(container, {
			theme: googleButtonTheme,
			size: "large",
			text: "continue_with",
			shape: "pill",
			width: 260,
			type: "standard",
			logo_alignment: "left",
		});

		renderedRef.current = true;

		// Wait for the iframe to be inserted before revealing the button.
		const revealWhenReady = () => {
			if (container.querySelector("iframe")) {
				setButtonReady(true);
				return true;
			}
			return false;
		};

		if (revealWhenReady()) return;

		const observer = new MutationObserver(() => {
			if (revealWhenReady()) observer.disconnect();
		});

		observer.observe(container, {
			childList: true,
			subtree: true,
		});

		return () => observer.disconnect();
	}, [scriptReady, googleButtonTheme]);

	return (
		<div className="flex h-10 min-h-10 w-full min-w-0 justify-center" aria-disabled={disabled}>
			<div
				ref={buttonRef}
				className={`h-10 w-[260px] overflow-hidden ${
					buttonReady ? "visible" : "invisible"
				} ${disabled ? "pointer-events-none opacity-40" : ""}`}
			/>
		</div>
	);
}
