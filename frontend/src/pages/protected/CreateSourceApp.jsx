import { useMutation, useQueryClient } from "@tanstack/react-query";
import axios from "axios";
import { Boxes, CreditCard, Shield, ShoppingCart } from "lucide-react";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router";

import { createSourceApp } from "@/api";
import Button from "@/components/Button";
import Container from "@/components/Container/Container";
import FormMessage from "@/components/Form/FormMessage";
import Input from "@/components/Input/Input";
import SelectInput from "@/components/Input/SelectInput";
import authenticatedClient from "@/core/api/customClient";
import { APP_NAME_RULES } from "@/shared/constants/HookFormValidatonRules";
import { SERVER_ERROR_MSG } from "@/shared/constants/messages";

export default function CreateSourceAppPage() {
	const {
		register,
		handleSubmit,
		setError,
		watch,
		clearErrors,
		formState: { errors, isSubmitting },
	} = useForm({
		mode: "onBlur",
		defaultValues: {
			appType: "auth-app",
		},
	});

	const navigate = useNavigate();
	const queryClient = useQueryClient();

	const { mutate } = useMutation({
		mutationFn: ({ appName, appType }) => {
			return createSourceApp({
				client: authenticatedClient,
				body: {
					name: appName,
					app_type: appType,
				},
			});
		},
		onSuccess: ({ data }) => {
			queryClient.invalidateQueries({
				queryKey: ["source-apps"],
			});
			navigate(`/dashboard/source-apps/${data.id}/batches`);
		},
		onError: (error) => {
			if (!axios.isAxiosError(error)) {
				setError("root", {
					type: "server",
					message: SERVER_ERROR_MSG,
				});
			} else {
				setError(error.response?.data.field || "root", {
					type: "server",
					message: error.response?.data.message || SERVER_ERROR_MSG,
				});
			}
		},
	});

	const appType = watch("appType");
	const appInfo = {
		"auth-app": {
			icon: Shield,
			title: "Authentication",
			description: "User authentication and authorization.",
		},
		"payment-app": {
			icon: CreditCard,
			title: "Payment",
			description: "Payment processing and billing.",
		},
		"order-app": {
			icon: ShoppingCart,
			title: "Order",
			description: "Order management and fulfillment.",
		},
	}[appType];

	const onSubmit = async ({ appName, appType }) => {
		clearErrors("root");

		mutate({
			appName,
			appType,
		});
	};

	return (
		<Container>
			<div className="border-border bg-surface rounded-3xl border p-8 shadow-md">
				<div className="mb-8 flex items-start gap-4">
					<div className="bg-primary-100 text-primary flex h-14 w-14 items-center justify-center rounded-2xl">
						<Boxes size={26} />
					</div>

					<div>
						<h2 className="text-t-primary text-2xl font-semibold">
							Create Application
						</h2>

						<p className="text-t-muted mt-1 text-sm">
							Register a new application for your logs incident analysis.
						</p>
					</div>
				</div>

				<FormMessage message={errors.root?.message} />

				<form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-6" noValidate>
					<Input
						label="Application Name"
						placeholder="Authentication"
						{...register("appName", APP_NAME_RULES)}
						error={errors.appName?.message}
					/>

					<SelectInput
						label="Application Type"
						{...register("appType", {
							required: "Application type is required",
						})}
						error={errors.appType?.message}
					>
						<option value="auth-app">Authentication</option>
						<option value="payment-app">Payment</option>
						<option value="order-app">Order</option>
					</SelectInput>

					<div className="border-border bg-elevated flex items-start gap-4 rounded-2xl border p-4">
						<div className="bg-accent-100 text-accent rounded-xl p-3">
							<appInfo.icon size={20} />
						</div>

						<div>
							<p className="text-t-primary font-medium">{appInfo.title}</p>

							<p className="text-t-muted mt-1 text-sm">{appInfo.description}</p>
						</div>
					</div>

					<Button type="submit" disabled={isSubmitting} className="mt-2 h-12 rounded-xl">
						{isSubmitting ? "Creating Application..." : "Create Application"}
					</Button>
				</form>
			</div>
		</Container>
	);
}
