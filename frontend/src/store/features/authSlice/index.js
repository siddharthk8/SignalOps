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
		setAccessToken: (state, action) => {
			state.user = { ...state.user, accessToken: action.payload };
		},
		updateNames: (state, action) => {
			state.user = {
				...state.user,
				firstName: action.payload.firstName,
				lastName: action.payload.lastName,
			};
		},
		updateProfileImage: (state, action) => {
			state.user = {
				...state.user,
				profileImage: action.payload,
			};
		},
		clearUser: (state) => {
			state.user = null;
			state.status = "idle";
		},
	},
});

export const { setUser, setAccessToken, updateNames, updateProfileImage, clearUser } =
	authSlice.actions;
export const authReducer = authSlice.reducer;
