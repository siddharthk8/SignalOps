import { useState } from "react";
import { useForm } from "react-hook-form";

import { EMAIL_RULES } from "@/shared/constants/HookFormValidatonRules";
import { FormStyle } from "@/shared/constants/Styles";

import Button from "../Button";
import Input from "../Input/Input";
import FormMessage from "./FormMessage";

export default function ForgotPasswordForm() {
	const {
		register,
		handleSubmit,
		formState: { errors, isSubmitting },
	} = useForm({ mode: "onBlur" });

	const [error, setError] = useState(null);
	const [success, setSuccess] = useState(false);

	const onSubmit = async ({ email }) => {
		setError(null);
		setSuccess(false);

		// ...
	};

	return (
		<>
			<FormMessage message={error?.message} />

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
	);
}
