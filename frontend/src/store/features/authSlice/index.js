import { createSlice } from "@reduxjs/toolkit";

import { getUserFromLS } from "@/shared/utils/userLocalStorage";

const LSUser = getUserFromLS();
const initialState = {
	user: LSUser,
	status: LSUser !== null ? "succeeded" : "idle", // 'idle' | 'pending' | 'succeeded' | 'failed'
};

const authSlice = createSlice({
	name: "auth",
	initialState,
	reducers: {
		setUser: (state, action) => {
			state.user = action.payload;
			state.status = "succeeded";
		},
		clearUser: (state) => {
			state.user = null;
			state.status = "idle";
		},
	},
});

export const { setUser, clearUser } = authSlice.actions;
export const authReducer = authSlice.reducer;
