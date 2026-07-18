import { createListenerMiddleware } from "@reduxjs/toolkit";

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
	effect: () => {
		removeUserFromLS();
	},
});
