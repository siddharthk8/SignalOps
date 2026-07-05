import { useState } from "react";
import { useForm } from "react-hook-form";
import { useDispatch } from "react-redux";

import AuthBgImage from "@/assets/images/auth-bg.jpg";
import Button from "@/components/Button";
import FormBottomLink from "@/components/Container/BottomLink";
import FormMessage from "@/components/Form/FormMessage";
import Checkbox from "@/components/Input/CheckboxInput";
import Input from "@/components/Input/Input";
import PasswordInput from "@/components/Input/PasswordInput";
import {
	EMAIL_RULES,
	FIRST_NAME_RULES,
	LAST_NAME_RULES,
	PASSWORD_RULES,
} from "@/shared/constants/HookFormValidatonRules";
import { FormStyle } from "@/shared/constants/Styles";

import AuthMainLayout from "../../layouts/Form/AuthMainLayout";

export default function SignupPage() {
	const {
		register,
		handleSubmit,
		setError,
		clearErrors,
		formState: { errors, isSubmitting },
	} = useForm({ mode: "onBlur" });

	const [success, setSuccess] = useState(false);

	const dispatch = useDispatch();

	const onSubmit = async ({ email, password, firstName, lastName }) => {
		clearErrors("root");
		setSuccess(false);

		// ...
	};

	return (
		<AuthMainLayout
			imageSrc={AuthBgImage}
			title="Create your account"
			description="Join us to access powerful tools, insights, and a personalized dashboard."
			headerText={"Sign up"}
			headerContent={"Create an account to get started"}
		>
			<>
				<FormMessage message={errors.root?.message} />

				{success && (
					<FormMessage
						type="success"
						message="Account created successfully. Please check your email to verify your account."
					/>
				)}

				<form onSubmit={handleSubmit(onSubmit)} noValidate className={FormStyle}>
					<div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
						<Input
							label="First name"
							placeholder="Siddharth"
							autoComplete="given-name"
							{...register("firstName", FIRST_NAME_RULES)}
							error={errors.firstName?.message}
						/>

						<Input
							label="Last name"
							placeholder="Kumar"
							autoComplete="family-name"
							{...register("lastName", LAST_NAME_RULES)}
							error={errors.lastName?.message}
						/>
					</div>

					<Input
						label="Email address"
						type="email"
						autoComplete="email"
						placeholder="you@company.com"
						{...register("email", EMAIL_RULES)}
						error={errors.email?.message}
					/>

					<PasswordInput
						label="Password"
						placeholder="••••••••"
						{...register("password", PASSWORD_RULES)}
						error={errors.password?.message}
					/>

					<Checkbox
						label="I agree to the"
						link={{ href: "/terms", text: "Terms & Conditions" }}
						error={errors.terms?.message}
						{...register("terms", {
							required: "You must accept the terms and conditions",
						})}
					/>

					<Button type="submit" disabled={isSubmitting}>
						{isSubmitting ? "Creating account…" : "Create account"}
					</Button>
				</form>

				<FormBottomLink
					className="py-4"
					text="Already have an account?"
					linkTextOrComp="Log In"
					to={"/login"}
				/>
			</>
		</AuthMainLayout>
	);
}
