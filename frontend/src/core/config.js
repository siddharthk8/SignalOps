const config = {
	apiUrl: String(import.meta.env.VITE_API_URL),
	isDev: String(import.meta.env.DEV) === "true",
};

export default config;
