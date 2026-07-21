import { useMutation, useQueryClient } from "@tanstack/react-query";
import axios from "axios";
import { useForm } from "react-hook-form";
import { useDispatch } from "react-redux";

import { createToken, getCurrentUser } from "@/api";
import AuthBgImage from "@/assets/images/auth-bg.jpg";
import Button from "@/components/Button";
import FormBottomLink from "@/components/Container/BottomLink";
import FormMessage from "@/components/Form/FormMessage";
import Input from "@/components/Input/Input";
import PasswordInput from "@/components/Input/PasswordInput";
import AuthMainLayout from "@/layouts/Form/AuthMainLayout";
import { EMAIL_RULES, PASSWORD_RULES } from "@/shared/constants/HookFormValidatonRules";
import { COMMON_ERROR_MSG, SERVER_ERROR_MSG } from "@/shared/constants/messages";
import { FormStyle } from "@/shared/constants/Styles";
import { setUser } from "@/store/features/authSlice";

export default function LoginPage() {
	const {
		register,
		handleSubmit,
		setError,
		clearErrors,
		formState: { errors },
	} = useForm({ mode: "onSubmit" });

	const dispatch = useDispatch();
	const queryClient = useQueryClient();

	const { mutate, isPending: isSubmitting } = useMutation({
		mutationFn: ({ email, password }) => {
			return createToken({
				body: {
					username: email,
					password,
				},
			});
		},
		onSuccess: async (loginResponse) => {
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

	const onSubmit = ({ email, password }) => {
		clearErrors("root");
		mutate({ email, password });
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

					<Button
						type="submit"
						disabled={isSubmitting}
						loading={isSubmitting}
						loadingText="Logging in…"
					>
						Log in
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
