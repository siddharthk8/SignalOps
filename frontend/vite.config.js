import { fileURLToPath } from "node:url";

import babel from "@rolldown/plugin-babel";
import tailwindcss from "@tailwindcss/vite";
import react, { reactCompilerPreset } from "@vitejs/plugin-react";
import { defineConfig } from "vite";

import packageJson from "./package.json";

// https://vite.dev/config/
export default defineConfig({
	plugins: [
		react(),
		tailwindcss(),
		babel({
			presets: [reactCompilerPreset()],
		}),
	],

	resolve: {
		alias: {
			"@": fileURLToPath(new URL("./src", import.meta.url)),
		},
	},

	define: {
		__APP_VERSION__: JSON.stringify(packageJson.version),
	},

	// Used only by `vite dev`
	server: {
		host: "localhost",
		port: 5173,
		strictPort: true,
	},

	// Used only by `vite preview`
	preview: {
		host: "localhost",
		port: 4173,
		strictPort: true,
	},
});
