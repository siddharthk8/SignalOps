import config from "@/core/config";

let initialized = false;
let activeCallback = null;

function dispatchCredential(response) {
	if (!response?.credential) return;

	activeCallback?.(response);
}

export function initializeGoogle(callback) {
	if (typeof window === "undefined") return false;

	const googleId = window.google?.accounts?.id;
	if (!googleId) return false;

	activeCallback = callback;

	if (!initialized) {
		googleId.initialize({
			client_id: config.googleClientId,
			callback: dispatchCredential,
			use_fedcm_for_button: true,
			auto_select: false,
		});

		initialized = true;
	}

	return true;
}

export function promptGoogleOneTap() {
	if (typeof window === "undefined") return false;

	const googleId = window.google?.accounts?.id;
	if (!googleId || !initialized) return false;

	googleId.prompt();
	return true;
}

export function setGoogleCallback(callback) {
	activeCallback = callback;

	return () => {
		if (activeCallback === callback) {
			activeCallback = null;
		}
	};
}
