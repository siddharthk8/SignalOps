import { getNewAccessToken } from "@/api";
import { createClient } from "@/api/client";
import config from "@/core/config";
import store from "@/store";
import { clearUser, setAccessToken } from "@/store/features/authSlice";
import { AxiosError, InternalAxiosRequestConfig } from "axios";

export const BASIC_API_CONFIG = {
	baseURL: config.apiUrl,
	throwOnError: true,
};

const authenticatedClient = createClient(BASIC_API_CONFIG);

// Request interceptor
authenticatedClient.instance.interceptors.request.use((config) => {
	const token = store.getState().auth.user?.accessToken;

	if (token) {
		config.headers.Authorization = `Bearer ${token}`;
	} else {
		throw new Error("No access token");
	}

	return config;
});

// Response interceptor
authenticatedClient.instance.interceptors.response.use(
	(response) => response,
	async (error: AxiosError) => {
		const originalRequest = error.config as InternalAxiosRequestConfig & {
			_retry?: boolean;
		};

		const status = error.response?.status;
		const message = error.response?.data?.message;

		if (
			status === 401 &&
			(message === "Access token expired." ||
				message === "Could not validate credentials.") &&
			originalRequest &&
			!originalRequest._retry
		) {
			originalRequest._retry = true;

			try {
				const refreshToken = store.getState().auth.user?.refreshToken;

				if (!refreshToken) {
					throw new Error("No refresh token");
				}

				// Refresh token request
				const refreshResponse = await getNewAccessToken({
					body: {
						refresh_token: refreshToken,
					},
				});

				const refreshResponseData = refreshResponse.data;
				if (!refreshResponseData) {
					throw new Error("No access token");
				}

				const { access_token } = refreshResponseData;

				// Save new access token
				store.dispatch(setAccessToken(access_token));

				// Update default Authorization header
				authenticatedClient.instance.defaults.headers.common["Authorization"] =
					`Bearer ${access_token}`;

				// Retry original request
				originalRequest.headers.Authorization = `Bearer ${access_token}`;

				return authenticatedClient.instance(originalRequest);
			} catch (refreshError) {
				store.dispatch(clearUser());
				return Promise.reject(refreshError);
			}
		}

		return Promise.reject(error);
	},
);

export default authenticatedClient;
