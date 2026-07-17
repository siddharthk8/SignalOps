export const getUserFromLS = () => {
	try {
		const stored = localStorage.getItem("user");
		return stored ? JSON.parse(stored) : null;
	} catch (err) {
		console.warn("Failed to load user from localStorage", err);
		return null;
	}
};

export const saveUserInLS = (user) => {
	try {
		localStorage.setItem("user", JSON.stringify(user));
	} catch (err) {
		console.warn("Failed to save user to localStorage", err);
	}
};

export const updateUserAccessTokenInLS = (accessToken) => {
	try {
		localStorage.setItem(
			"user",
			JSON.stringify({
				...getUserFromLS(),
				accessToken,
			}),
		);
	} catch (err) {
		console.warn("Failed to save user to localStorage", err);
	}
};

export const removeUserFromLS = () => {
	try {
		localStorage.removeItem("user");
	} catch (err) {
		console.warn("Failed to remove user from localStorage", err);
	}
};
