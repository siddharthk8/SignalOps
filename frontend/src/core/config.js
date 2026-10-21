const config = {
	googleClientId: String(import.meta.env.VITE_GOOGLE_CLIENT_ID),
	apiUrl: String(import.meta.env.VITE_API_URL),
	isDev: String(import.meta.env.DEV) === "development",
};

export default config;
