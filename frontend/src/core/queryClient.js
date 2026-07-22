import { MutationCache, QueryCache, QueryClient } from "@tanstack/react-query";
import axios from "axios";

import config from "@/core/config";

// tanstack query client
const queryClient = new QueryClient({
	queryCache: new QueryCache({
		onError: (error, query) => {
			if (config.isDev) {
				console.error("Query Error:\n", query.queryKey, "\n", error);
			}
		},
	}),
	mutationCache: new MutationCache({
		onError: (error, variables, context, mutation) => {
			if (config.isDev) {
				console.error("Mutation Error:\n", mutation.options.mutationKey, "\n", error);
			}
		},
	}),
	defaultOptions: {
		queries: {
			staleTime: 5 * 60 * 1000, // 5 minutes
			gcTime: 15 * 60 * 1000, // 15 minutes
			retry: (failureCount, error) => {
				if (!axios.isAxiosError(error)) {
					return false;
				}

				if (config.isDev) {
					return false;
				}

				const status = error.response?.status;
				// Network error (no response)
				if (!status) {
					return failureCount < 2;
				}
				// Don't retry client errors
				if (status >= 400 && status < 500) {
					return false;
				}

				// Retry server errors
				return failureCount < 2;
			},
		},
		mutations: {
			retry: false,
		},
	},
});

export default queryClient;
