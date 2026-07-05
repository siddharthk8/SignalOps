import { createListenerMiddleware } from "@reduxjs/toolkit";

import { removeUserFromLS, saveUserInLS } from "../shared/utils/userLocalStorage";
import { clearUser, setUser } from "./features/authSlice";

export const listenerMiddleware = createListenerMiddleware();

listenerMiddleware.startListening({
	actionCreator: setUser,
	effect: (action) => {
		saveUserInLS(action.payload);
	},
});

listenerMiddleware.startListening({
	actionCreator: clearUser,
	effect: () => {
		removeUserFromLS();
	},
});
