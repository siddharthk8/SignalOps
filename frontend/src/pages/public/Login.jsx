import { useForm } from "react-hook-form";
import { useDispatch } from "react-redux";

import AuthBgImage from "@/assets/images/auth-bg.jpg";
import Button from "@/components/Button";
import FormBottomLink from "@/components/Container/BottomLink";
import FormMessage from "@/components/Form/FormMessage";
import Input from "@/components/Input/Input";
import PasswordInput from "@/components/Input/PasswordInput";
import AuthMainLayout from "@/layouts/Form/AuthMainLayout";
import { EMAIL_RULES, PASSWORD_RULES } from "@/shared/constants/HookFormValidatonRules";
import { FormStyle } from "@/shared/constants/Styles";

export default function LoginPage() {
	const {
		register,
		handleSubmit,
		setError,
		clearErrors,
		formState: { errors, isSubmitting },
	} = useForm({ mode: "onBlur" });

	const dispatch = useDispatch();

	const onSubmit = async ({ email, password }) => {
		clearErrors("root");

		// ...
		// dispatch(setUser(user));
	};

	return (
		<AuthMainLayout
			imageSrc={AuthBgImage}
			title="Welcome back"
			description="Secure access to your dashboard, insights, and tools — all in one place."
			headerText={"Log In"}
			headerContent={"Log In to you account"}
		>
			<>
				<FormMessage message={errors.root?.message} />

				<form onSubmit={handleSubmit(onSubmit)} noValidate className={`${FormStyle}`}>
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

					<Button type="submit" disabled={isSubmitting}>
						{isSubmitting ? "Logging in…" : "Log in"}
					</Button>
				</form>

				<div className="flex flex-col items-center gap-2 py-4">
					<FormBottomLink
						text="Don’t have an account?"
						linkTextOrComp="Sign Up"
						to={"/signup"}
					/>
					<FormBottomLink
						text="Forgot your password?"
						linkTextOrComp="Reset it here"
						to={"/forgot-password"}
					/>
				</div>
			</>
		</AuthMainLayout>
	);
}
