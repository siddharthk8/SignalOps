import { useState } from "react";
import { useForm } from "react-hook-form";

import AuthBgImage from "@/assets/images/auth-bg.jpg";
import Button from "@/components/Button";
import FormMessage from "@/components/Form/FormMessage";
import Input from "@/components/Input/Input";
import AuthRecoveryLayout from "@/layouts/Form/AuthRecoveryLayout";
import { EMAIL_RULES } from "@/shared/constants/HookFormValidatonRules";
import { FormStyle } from "@/shared/constants/Styles";

export default function ForgotPasswordPage() {
	const {
		register,
		handleSubmit,
		setError,
		clearErrors,
		formState: { errors, isSubmitting },
	} = useForm({ mode: "onBlur" });

	const [success, setSuccess] = useState(false);

	const onSubmit = async ({ email }) => {
		clearErrors("root");
		setSuccess(false);

		// ...
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

				{success && <FormMessage message="..." />}

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
