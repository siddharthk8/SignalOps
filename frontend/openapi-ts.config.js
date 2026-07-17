import { defineConfig } from "@hey-api/openapi-ts";

// npm run openapi-ts
export default defineConfig({
	input: "http://127.0.0.1:8000/openapi.json",
	output: "src/api",
	plugins: [
		{
			name: "@hey-api/typescript",
			comments: false,
		},
		"@hey-api/client-fetch",
		"@hey-api/sdk",
	],
});
