import { createListenerMiddleware } from "@reduxjs/toolkit";

import queryClient from "@/core/queryClient";

import { removeUserFromLS, saveUserInLS, updateDataInLS } from "../shared/utils/userLocalStorage";
import {
	clearUser,
	setAccessToken,
	setUser,
	updateNames,
	updateProfileImage,
} from "./features/authSlice";

export const listenerMiddleware = createListenerMiddleware();

listenerMiddleware.startListening({
	actionCreator: setUser,
	effect: (action) => {
		saveUserInLS(action.payload);
	},
});

listenerMiddleware.startListening({
	actionCreator: setAccessToken,
	effect: (action) => {
		updateDataInLS({ accessToken: action.payload });
	},
});

listenerMiddleware.startListening({
	actionCreator: updateProfileImage,
	effect: (action) => {
		updateDataInLS({ profileImage: action.payload });
	},
});

listenerMiddleware.startListening({
	actionCreator: updateNames,
	effect: (action) => {
		updateDataInLS(action.payload);
	},
});

listenerMiddleware.startListening({
	actionCreator: clearUser,
	effect: async () => {
		// Stop any in-flight requests before clearing the cache.
		await queryClient.cancelQueries();

		// Clear all cached data so the next signed-in user starts with a fresh cache.
		queryClient.clear();

		removeUserFromLS();
	},
});
