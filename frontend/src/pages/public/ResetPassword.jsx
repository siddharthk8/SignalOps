import { useMutation } from "@tanstack/react-query";
import axios from "axios";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { useSearchParams } from "react-router";

import { resetPassword } from "@/api";
import AuthBgImage from "@/assets/images/auth-bg.jpg";
import Button from "@/components/Button";
import FormMessage from "@/components/Form/FormMessage";
import PasswordInput from "@/components/Input/PasswordInput";
import { PASSWORD_RULES } from "@/shared/constants/HookFormValidatonRules";
import { SERVER_ERROR_MSG } from "@/shared/constants/messages";
import { FormStyle } from "@/shared/constants/Styles";

import AuthRecoveryLayout from "../../layouts/Form/AuthRecoveryLayout";

export default function ResetPasswordPage() {
	const {
		register,
		handleSubmit,
		watch,
		setError,
		clearErrors,
		formState: { errors, isSubmitting },
	} = useForm({ mode: "onBlur" });

	const [searchParams] = useSearchParams();
	const token = searchParams.get("token");

	const [success, setSuccess] = useState(false);
	const newPassword = watch("newPassword", "");

	const { mutate: mutateOnSubmit } = useMutation({
		mutationFn: ({ newPassword }) => {
			return resetPassword({
				body: {
					token: token,
					new_password: newPassword,
				},
			});
		},
		onSuccess: () => {
			setSuccess(true);
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

	const onSubmit = async ({ newPassword, code }) => {
		clearErrors("root");
		setSuccess(false);

		mutateOnSubmit({
			token: code,
			newPassword,
		});
	};

	return (
		<AuthRecoveryLayout
			imageSrc={AuthBgImage}
			title="Set a new password"
			description="Secure your account by choosing a strong new password."
			headerText="Reset Password"
			headerContent="Enter your new password below to update your account credentials."
		>
			<>
				<FormMessage message={errors.root?.message} />

				{success && (
					<FormMessage
						type="success"
						message="Your password has been reset successfully."
					/>
				)}
				<form onSubmit={handleSubmit(onSubmit)} noValidate className={FormStyle}>
					<PasswordInput
						label="New Password"
						placeholder="Enter new password"
						{...register("newPassword", PASSWORD_RULES)}
						error={errors.newPassword?.message}
					/>

					<PasswordInput
						label="Confirm Password"
						placeholder="Re-enter new password"
						{...register("confirmPassword", {
							...PASSWORD_RULES,
							validate: {
								...PASSWORD_RULES.validate,
								areSame: (value) =>
									value === newPassword || "Passwords do not match",
							},
						})}
						error={errors.confirmPassword?.message}
					/>

					<Button type="submit" disabled={isSubmitting}>
						{isSubmitting ? "Resetting…" : "Reset Password"}
					</Button>
				</form>
			</>
		</AuthRecoveryLayout>
	);
}
