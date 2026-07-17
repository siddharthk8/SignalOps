import { useMutation } from "@tanstack/react-query";
import axios from "axios";
import { useForm } from "react-hook-form";
import { useDispatch } from "react-redux";

import { changePassword } from "@/api";
import AuthBgImage from "@/assets/images/auth-bg.jpg";
import Button from "@/components/Button";
import FormMessage from "@/components/Form/FormMessage";
import PasswordInput from "@/components/Input/PasswordInput";
import authenticatedClient from "@/core/api/customClient";
import AuthRecoveryLayout from "@/layouts/Form/AuthRecoveryLayout";
import { PASSWORD_RULES } from "@/shared/constants/HookFormValidatonRules";
import { SERVER_ERROR_MSG } from "@/shared/constants/messages";
import { FormStyle } from "@/shared/constants/Styles";
import { clearUser } from "@/store/features/authSlice";

export default function ChangePasswordPage() {
	const {
		register,
		handleSubmit,
		watch,
		setError,
		clearErrors,
		formState: { errors, isSubmitting },
	} = useForm({ mode: "onBlur" });

	const dispatch = useDispatch();
	const currentPassword = watch("currentPassword", "");
	const newPassword = watch("newPassword", "");

	const { mutate } = useMutation({
		mutationFn: ({ newPassword, currentPassword }) => {
			return changePassword({
				client: authenticatedClient,
				body: {
					current_password: currentPassword,
					new_password: newPassword,
				},
			});
		},
		onSuccess: () => {
			dispatch(clearUser());
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

	const onSubmit = async ({ newPassword, currentPassword }) => {
		clearErrors("root");

		mutate({
			currentPassword,
			newPassword,
		});
	};

	return (
		<AuthRecoveryLayout
			imageSrc={AuthBgImage}
			title="Change your password"
			description="Update your password to keep your account secure."
			headerText="Change Password"
			headerContent="Enter your current and new password."
		>
			<>
				<FormMessage message={errors.root?.message} />

				{/* {success && (
					<FormMessage
						type="success"
						message="Your password has been changed successfully."
					/>
				)} */}
				<form onSubmit={handleSubmit(onSubmit)} noValidate className={FormStyle}>
					<PasswordInput
						label="Current Password"
						placeholder="Enter current password"
						{...register("currentPassword", PASSWORD_RULES)}
						error={errors.currentPassword?.message}
					/>

					<PasswordInput
						label="New Password"
						placeholder="Enter new password"
						{...register("newPassword", {
							...PASSWORD_RULES,
							validate: {
								...PASSWORD_RULES.validate,
								areSame: (value) =>
									value !== currentPassword ||
									"Current and New password should not be same.",
							},
						})}
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
						{isSubmitting ? "Changing..." : "Change Password"}
					</Button>
				</form>
			</>
		</AuthRecoveryLayout>
	);
}
