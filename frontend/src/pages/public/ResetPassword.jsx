import { useState } from "react";
import { useForm } from "react-hook-form";
import { useSearchParams } from "react-router";

import AuthBgImage from "@/assets/images/auth-bg.jpg";
import Button from "@/components/Button";
import FormBottomLink from "@/components/Container/BottomLink";
import FormMessage from "@/components/Form/FormMessage";
import PasswordInput from "@/components/Input/PasswordInput";
import { PASSWORD_RULES } from "@/shared/constants/HookFormValidatonRules";
import { FormStyle } from "@/shared/constants/Styles";
import useResendCoolDown from "@/shared/hooks/useResendCoolDownTime";

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
	const { formattedTime, isCooldownActive, startCooldown } = useResendCoolDown(120); // 2 minutes

	const [searchParams] = useSearchParams();
	const token = searchParams.get("token");

	const [success, setSuccess] = useState(false);
	const [resendLoading, setResendLoading] = useState(false);
	const [resendSuccess, setResendSuccess] = useState(false);

	const newPassword = watch("newPassword", "");

	const onSubmit = async ({ newPassword, code }) => {
		clearErrors("root");
		setSuccess(false);

		// ...
	};

	const handleResend = async () => {
		clearErrors("root");
		setResendSuccess(false);
		setResendLoading(true);

		// ...
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

				{resendSuccess && (
					<FormMessage
						type="success"
						message="A new verification code has been sent to your email."
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

				<div className="flex flex-col items-center gap-2 py-4">
					<FormBottomLink
						text="Didn’t receive the code?"
						linkTextOrComp={
							<button
								type="button"
								disabled={
									resendLoading ||
									isCooldownActive ||
									isSubmitting || // ❌ Disable resend while submitting password reset
									success // ❌ Disable resend after success
								}
								onClick={handleResend}
								className="disabled:opacity-50"
							>
								{resendLoading
									? "Resending…"
									: isCooldownActive
										? `Resend in ${formattedTime}`
										: "Resend"}
							</button>
						}
					/>
				</div>
			</>
		</AuthRecoveryLayout>
	);
}
