import config from "@/core/config";

let initialized = false;
let activeCallback = null;

function dispatchCredential(response) {
	if (!response?.credential) {
		// console.error("[Google Identity] No credential received");
		return;
	}

	activeCallback?.(response);
}

export function initializeGoogle(callback) {
	if (typeof window === "undefined") return false;

	if (!window.google?.accounts?.id) {
		return false;
	}

	activeCallback = callback;
	if (initialized) {
		return true;
	}

	window.google.accounts.id.initialize({
		client_id: config.googleClientId,
		callback: dispatchCredential,
		use_fedcm_for_button: true,
	});

	initialized = true;
	// console.log("[Google Identity] Initialized once");
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
