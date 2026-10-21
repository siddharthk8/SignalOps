import { useMutation, useQueryClient } from "@tanstack/react-query";
import axios from "axios";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { useDispatch } from "react-redux";
import { useLocation, useNavigate } from "react-router";

import { createUser, getCurrentUser } from "@/api";
import AuthBgImage from "@/assets/images/auth-bg.jpg";
import Button from "@/components/Button";
import FormBottomLink from "@/components/Container/BottomLink";
import FormMessage from "@/components/Form/FormMessage";
import AuthLoginSignup from "@/components/Google/GoogleLoginSignup";
import Input from "@/components/Input/Input";
import PasswordInput from "@/components/Input/PasswordInput";
import {
	EMAIL_RULES,
	FIRST_NAME_RULES,
	LAST_NAME_RULES,
	PASSWORD_RULES,
} from "@/shared/constants/HookFormValidatonRules";
import { COMMON_ERROR_MSG, SERVER_ERROR_MSG } from "@/shared/constants/messages";
import { FormStyle } from "@/shared/constants/Styles";
import { setUser } from "@/store/features/authSlice";

import AuthMainLayout from "../../layouts/Form/AuthMainLayout";

export default function SignupPage() {
	const {
		register,
		handleSubmit,
		setError,
		clearErrors,
		formState: { errors },
	} = useForm({ mode: "onBlur" });
	const location = useLocation();
	const dispatch = useDispatch();

	// Check if the current pathname matches the screen
	const screenIsActive = location.pathname === "/signup";

	const navigate = useNavigate();
	const queryClient = useQueryClient();

	const [password, setPassword] = useState();

	const handleLoginSuccess = async (loginResponse) => {
		const tokenData = loginResponse.data;
		if (!tokenData) {
			throw new Error(COMMON_ERROR_MSG);
		}
		const userResponse = await queryClient.fetchQuery({
			queryKey: ["currentUser"],
			queryFn: () =>
				getCurrentUser({
					headers: {
						Authorization: `Bearer ${tokenData.access_token}`,
					},
				}),
		});
		const user = userResponse.data;
		if (!user) {
			throw new Error(COMMON_ERROR_MSG);
		}

		dispatch(
			setUser({
				accessToken: tokenData.access_token,
				refreshToken: tokenData.refresh_token,
				id: user.id,
				email: user.email,
				firstName: user.first_name,
				lastName: user.last_name,
				profileImage: user.profile_image_path,
			}),
		);
	};

	const { mutate, isPending: isSubmitting } = useMutation({
		mutationFn: ({ email, firstName }) => {
			return createUser({
				body: {
					first_name: firstName,
					email: email,
				},
			});
		},
		onSuccess: async (signupResponse, variables) => {
			navigate("/email-verification", {
				state: {
					email: variables.email,
					lastName: variables.lastName,
					password: password,
					firstName: variables.firstName,
				},
			});
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

	const onSubmit = async ({ email, password, firstName, lastName }) => {
		clearErrors("root");
		setPassword(password);
		mutate({
			firstName,
			lastName,
			password,
			email,
		});
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

				<form onSubmit={handleSubmit(onSubmit)} noValidate className={FormStyle}>
					<div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
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
						placeholder="you@example.com"
						{...register("email", EMAIL_RULES)}
						error={errors.email?.message}
					/>

					<PasswordInput
						label="Password"
						placeholder="••••••••"
						{...register("password", PASSWORD_RULES)}
						error={errors.password?.message}
					/>

					{/* <Checkbox
						label="I agree to the"
						link={{ href: "/terms", text: "Terms & Conditions" }}
						error={errors.terms?.message}
						{...register("terms", {
							required: "You must accept the terms and conditions",
						})}
					/> */}

					<Button
						type="submit"
						disabled={isSubmitting}
						loading={isSubmitting}
						loadingText="Creating account…"
					>
						Create account
					</Button>

					<div className="relative flex items-center">
						<div className="border-border grow border-t" />
						<span className="text-t-muted mx-4 shrink-0 text-xs">OR</span>
						<div className="border-border grow border-t" />
					</div>

					<AuthLoginSignup
						isActive={screenIsActive}
						onLoginSuccess={handleLoginSuccess}
					/>
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
