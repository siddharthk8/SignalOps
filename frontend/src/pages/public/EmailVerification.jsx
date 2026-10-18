import { useMutation, useQueryClient } from "@tanstack/react-query";
import axios from "axios";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { useDispatch } from "react-redux";
import { useLocation } from "react-router";

import { createToken, verifyCreateUserEmail } from "@/api";
// import { verifyEmail } from "@/api";
import AuthBgImage from "@/assets/images/auth-bg.jpg";
import Button from "@/components/Button";
import FormMessage from "@/components/Form/FormMessage";
import Input from "@/components/Input/Input";
import AuthRecoveryLayout from "@/layouts/Form/AuthRecoveryLayout";
import { COMMON_ERROR_MSG, SERVER_ERROR_MSG } from "@/shared/constants/messages";
import { FormStyle } from "@/shared/constants/Styles";
import { setUser } from "@/store/features/authSlice";

export default function EmailVerificationPage() {
	const {
		register,
		handleSubmit,
		setError,
		clearErrors,
		formState: { errors },
	} = useForm({ mode: "onBlur" });

	const dispatch = useDispatch();
	const queryClient = useQueryClient();

	const location = useLocation();
	const user = location.state;

	const [success, setSuccess] = useState(false);

	const { mutate, isPending: isSubmitting } = useMutation({
		mutationFn: ({ otp }) => {
			return verifyCreateUserEmail({
				body: {
					otp,
					email: user.email,
					first_name: user.firstName,
					last_name: user.lastName,
					password: user.password,
				},
			});
		},
		onSuccess: async (signupResponse) => {
			const userData = signupResponse.data;

			if (!userData) {
				throw new Error(COMMON_ERROR_MSG);
			}

			const tokenResponse = await queryClient.fetchQuery({
				queryKey: ["createToken"],
				queryFn: () =>
					createToken({
						body: {
							username: userData.email,
							password: user.password,
						},
					}),
			});

			const tokenData = tokenResponse.data;
			if (!tokenData) {
				throw new Error(COMMON_ERROR_MSG);
			}

			dispatch(
				setUser({
					accessToken: tokenData.access_token,
					refreshToken: tokenData.refresh_token,
					id: userData.id,
					email: userData.email,
					firstName: userData.first_name,
					lastName: userData.last_name,
					profileImage: userData.profile_image_path,
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
				setError(error.response?.data?.field || "root", {
					type: "server",
					message: error.response?.data?.message || SERVER_ERROR_MSG,
				});
			}
		},
	});

	const onSubmit = ({ otp }) => {
		clearErrors();
		setSuccess(false);
		mutate({ otp });
	};

	return (
		<AuthRecoveryLayout
			imageSrc={AuthBgImage}
			title="Verify your email"
			description="We've sent a verification code to your email address."
			headerText="Email Verification"
			headerContent="Enter the one-time password (OTP) sent to your email to verify your account."
		>
			<>
				<FormMessage message={errors.root?.message} />

				{success && (
					<FormMessage
						type="success"
						message="Your email has been verified successfully."
					/>
				)}

				<form onSubmit={handleSubmit(onSubmit)} noValidate className={FormStyle}>
					<Input
						label="Verification code"
						type="text"
						placeholder="Enter your OTP"
						autoComplete="one-time-code"
						inputMode="numeric"
						maxLength={6}
						{...register("otp", {
							required: "Verification code is required.",
							pattern: {
								value: /^\d{6}$/,
								message: "Enter a valid 6-digit OTP.",
							},
						})}
						error={errors.otp?.message}
					/>

					<Button
						type="submit"
						disabled={isSubmitting}
						loading={isSubmitting}
						loadingText="Verifying…"
					>
						Verify email
					</Button>
				</form>
			</>
		</AuthRecoveryLayout>
	);
}
