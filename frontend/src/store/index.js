import { configureStore } from "@reduxjs/toolkit";

import { authReducer } from "./features/authSlice";
import { listenerMiddleware } from "./listenerMiddleware";

const store = configureStore({
	reducer: {
		auth: authReducer,
	},
	middleware: (getDefaultMiddleware) =>
		getDefaultMiddleware().prepend(listenerMiddleware.middleware),
});

export default store;
