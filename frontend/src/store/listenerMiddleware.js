import { createListenerMiddleware } from "@reduxjs/toolkit";

import {
	removeUserFromLS,
	saveUserInLS,
	updateUserAccessTokenInLS,
} from "../shared/utils/userLocalStorage";
import { clearUser, setAccessToken, setUser } from "./features/authSlice";

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
		updateUserAccessTokenInLS(action.payload);
	},
});

listenerMiddleware.startListening({
	actionCreator: clearUser,
	effect: () => {
		removeUserFromLS();
	},
});
