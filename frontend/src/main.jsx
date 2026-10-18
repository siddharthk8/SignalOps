import "./index.css";

import { QueryClientProvider } from "@tanstack/react-query";
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { Provider } from "react-redux";
import { createBrowserRouter, RouterProvider } from "react-router";

import { client } from "@/api/client.gen";
import { BASIC_API_CONFIG } from "@/core/api/customClient";
import queryClient from "@/core/queryClient";
import DashboardLayout from "@/layouts/DashboardLayout";
import Layout from "@/layouts/Layout.jsx";
// pages
import ErrorPage from "@/pages/ErrorPage";
import NotFoundPage from "@/pages/NotFoundPage";
import BatchDetailsPage from "@/pages/protected/BatchDetails.jsx";
import BatchesPage from "@/pages/protected/Batches.jsx";
import ChangePasswordPage from "@/pages/protected/ChangePassword";
import CreateSourceAppPage from "@/pages/protected/CreateSourceApp";
import DashboardPage from "@/pages/protected/Dashboard";
import IngestLogsPage from "@/pages/protected/IngestLogs";
import ProfilePage from "@/pages/protected/Profile";
import SourceAppsPage from "@/pages/protected/SourceApps";
import EmailVerificationPage from "@/pages/public/EmailVerification";
import ForgotPasswordPage from "@/pages/public/ForgotPassword";
import LoginPage from "@/pages/public/Login";
import ResetPasswordPage from "@/pages/public/ResetPassword";
import SignupPage from "@/pages/public/Signup";
// redux store
import store from "@/store";

import App from "./App.jsx";
import ProtectedRoute from "./components/Routes/ProtectedRoute.jsx";
import PublicRoute from "./components/Routes/PublicRoute.jsx";

const router = createBrowserRouter([
	{
		path: "/",
		element: <Layout />,
		errorElement: <ErrorPage />,
		children: [
			// Default Page
			{
				index: true,
				element: <App />,
			},
			// Public routes
			{
				element: <PublicRoute />,
				children: [
					{
						path: "login",
						element: <LoginPage />,
					},
					{
						path: "signup",
						element: <SignupPage />,
					},
					{
						path: "forgot-password",
						element: <ForgotPasswordPage />,
					},
					{
						path: "reset-password",
						element: <ResetPasswordPage />,
					},
					{
						path: "email-verification",
						element: <EmailVerificationPage />,
					},
				],
			},
			// Protected routes
			{
				element: <ProtectedRoute />,
				children: [
					{
						path: "dashboard",
						element: <DashboardLayout />,
						children: [
							{
								index: true,
								element: <DashboardPage />,
							},
							{
								path: "source-apps",
								element: <SourceAppsPage />,
							},
							{
								path: "source-apps/:sourceAppId/batches",
								element: <BatchesPage />,
							},
							{
								path: "source-apps/:sourceAppId/batches/:batchId",
								element: <BatchDetailsPage />,
							},
							{
								path: "source-apps/:sourceAppId/batches/ingest-logs",
								element: <IngestLogsPage />,
							},
							{
								path: "create-source-app",
								element: <CreateSourceAppPage />,
							},
						],
					},

					{
						path: "profile",
						element: <ProfilePage />,
					},
					{
						path: "change-password",
						element: <ChangePasswordPage />,
					},
				],
			},
			// 404
			{
				path: "*",
				element: <NotFoundPage />,
			},
		],
	},
]);

// api client config
client.setConfig(BASIC_API_CONFIG);

createRoot(document.getElementById("root")).render(
	<StrictMode>
		<QueryClientProvider client={queryClient}>
			<Provider store={store}>
				<RouterProvider router={router} />
			</Provider>
		</QueryClientProvider>
	</StrictMode>,
);
