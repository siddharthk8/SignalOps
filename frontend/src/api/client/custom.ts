import { createClient } from "@/api/client/client.gen";
import store from "@/store";

export const BASIC_API_CONFIG = {
	baseUrl: "http://127.0.0.1:8000",
	throwOnError: true,
};

export const authenticatedClient = createClient({
	...BASIC_API_CONFIG,
	auth: () => {
		const token = store.getState().auth.user?.accessToken;
		return token ? `Bearer ${token}` : undefined;
	},
});

authenticatedClient.interceptors.request.use((request) => {
	request.headers.set("Authorization", `Bearer ${store.getState().auth.user?.accessToken}`);
	return request;
});
