import { useMutation } from "@tanstack/react-query";
import axios from "axios";
import { useState } from "react";
import { useForm } from "react-hook-form";

import { forgotPassword } from "@/api";
import AuthBgImage from "@/assets/images/auth-bg.jpg";
import Button from "@/components/Button";
import FormMessage from "@/components/Form/FormMessage";
import Input from "@/components/Input/Input";
import AuthRecoveryLayout from "@/layouts/Form/AuthRecoveryLayout";
import { EMAIL_RULES } from "@/shared/constants/HookFormValidatonRules";
import { SERVER_ERROR_MSG } from "@/shared/constants/messages";
import { FormStyle } from "@/shared/constants/Styles";

export default function ForgotPasswordPage() {
	const {
		register,
		handleSubmit,
		setError,
		clearErrors,
		reset,
		formState: { errors, isSubmitting },
	} = useForm({ mode: "onBlur" });

	const [success, setSuccess] = useState(false);

	const { mutate } = useMutation({
		mutationFn: ({ email }) => {
			return forgotPassword({
				body: {
					email: email,
				},
			});
		},
		onSuccess: () => {
			setSuccess(true);
			reset();
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

	const onSubmit = ({ email }) => {
		clearErrors("root");
		setSuccess(false);
		mutate({ email });
	};

	return (
		<AuthRecoveryLayout
			imageSrc={AuthBgImage}
			title="Forgot your password?"
			description="No worries! Enter your email and we'll send you instructions to reset it."
			headerText="Forgot Password"
			headerContent="Enter the email associated with your account to receive a reset link."
		>
			<>
				<FormMessage message={errors.root?.message} />

				{success && (
					<FormMessage
						type="success"
						message="If an account exists, a reset code has been sent to your email."
					/>
				)}

				<form onSubmit={handleSubmit(onSubmit)} noValidate className={FormStyle}>
					<Input
						label="Email address"
						type="email"
						placeholder="you@example.com"
						autoComplete="email"
						{...register("email", EMAIL_RULES)}
						error={errors.email?.message}
					/>

					<Button type="submit" disabled={isSubmitting}>
						{isSubmitting ? "Sending reset link…" : "Send reset link"}
					</Button>
				</form>
			</>
		</AuthRecoveryLayout>
	);
}
