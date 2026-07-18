import { useMutation } from "@tanstack/react-query";
import axios from "axios";
import { Trash2 } from "lucide-react";
import { useState } from "react";
import { Controller, useForm } from "react-hook-form";
import { useDispatch, useSelector } from "react-redux";

import {
	deleteCurrentUser,
	deleteProfileImage,
	updateCurrentUser,
	uploadProfileImage,
} from "@/api";
import Button from "@/components/Button";
import Container from "@/components/Container/Container";
import FormMessage from "@/components/Form/FormMessage";
import Input from "@/components/Input/Input";
import ProfileImagePicker from "@/components/Input/ProfileImagePicker";
import authenticatedClient from "@/core/api/customClient";
import {
	FIRST_NAME_RULES_NRQ,
	LAST_NAME_RULES_NRQ,
} from "@/shared/constants/HookFormValidatonRules";
import { SERVER_ERROR_MSG } from "@/shared/constants/messages";
import { FormStyle } from "@/shared/constants/Styles";
import { clearUser, updateNames, updateProfileImage } from "@/store/features/authSlice";

function ProfilePage() {
	const [success, setSuccess] = useState(false);
	const dispatch = useDispatch();
	const user = useSelector((state) => state.auth.user);

	const { register, handleSubmit, setError, clearErrors, control, reset, watch, formState } =
		useForm({
			mode: "onBlur",
			defaultValues: {
				profileImage: user.profileImage,
				firstName: user.firstName,
				lastName: user.lastName,
			},
		});

	/**
	 * TODO:
	 * RHF `formState.isDirty` stops updating correctly after the first successful
	 * submission unless `watch()` is subscribed.
	 * This might be a bug in RHF - report ISSUE, submit PR if possible, and for now use watch().
	 */
	watch();

	const { isDirty, dirtyFields, errors, isSubmitting } = formState;

	const { mutate: mutateDelete, isSubmitting: isDeleting } = useMutation({
		mutationFn: () => {
			return deleteCurrentUser({
				client: authenticatedClient,
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

	const { mutate } = useMutation({
		mutationFn: ({ firstName, lastName }) => {
			return updateCurrentUser({
				client: authenticatedClient,
				body: {
					first_name: firstName,
					last_name: lastName,
				},
			});
		},
		onSuccess: ({ data }) => {
			reset({
				firstName: data.first_name,
				lastName: data.last_name,
				profileImage: data.profile_image_path,
			});
			dispatch(
				updateNames({
					firstName: data.first_name,
					lastName: data.last_name,
				}),
			);
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

	const { mutate: mutateFile, isSubmitting: isSubmittingFile } = useMutation({
		mutationFn: ({ profileImage }) => {
			if (!profileImage) {
				return deleteProfileImage({
					client: authenticatedClient,
				});
			} else {
				return uploadProfileImage({
					client: authenticatedClient,
					body: {
						file: profileImage,
					},
				});
			}
		},
		onSuccess: ({ data }) => {
			reset({
				firstName: data.first_name,
				lastName: data.last_name,
				profileImage: data.profile_image_path,
			});
			dispatch(updateProfileImage(data.profile_image_path));
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

	const onSubmit = ({ firstName, lastName, profileImage }) => {
		clearErrors("root");
		setSuccess(false);

		if (dirtyFields.firstName && dirtyFields.lastName) {
			mutate({
				firstName,
				lastName,
			});
		} else if (dirtyFields.firstName) {
			mutate({ firstName });
		} else if (dirtyFields.lastName) {
			mutate({ lastName });
		}

		if (dirtyFields.profileImage) {
			mutateFile({ profileImage });
		}
	};

	return (
		<Container>
			<div className="space-y-8">
				{/* Header */}
				<section>
					<h1 className="font-['Space_Grotesk'] text-3xl font-bold tracking-tight">
						Profile Settings
					</h1>

					<p className="text-t-muted mt-2 text-sm">
						Manage your account information and preferences.
					</p>
				</section>

				<FormMessage message={errors.root?.message} />

				{success && (
					<FormMessage
						type="success"
						message="Your profile has been updated successfully."
					/>
				)}
				<form onSubmit={handleSubmit(onSubmit)} noValidate className={FormStyle}>
					<Controller
						name="profileImage"
						control={control}
						render={({ field }) => (
							<ProfileImagePicker
								value={field.value}
								loading={isSubmittingFile}
								onChange={field.onChange}
							/>
						)}
					/>

					<div className="grid gap-4 md:grid-cols-2">
						<Input
							label="First Name"
							placeholder="Enter first name"
							{...register("firstName", FIRST_NAME_RULES_NRQ)}
							error={errors.firstName?.message}
						/>

						<Input
							label="Last Name"
							placeholder="Enter last name"
							{...register("lastName", LAST_NAME_RULES_NRQ)}
							error={errors.lastName?.message}
						/>
					</div>

					<Input label="Email Address" type="email" value={user.email} disabled />

					<div className="flex justify-end">
						<Button
							type="submit"
							loading={isSubmitting || isSubmittingFile}
							loadingText="Saving..."
							disabled={!isDirty}
						>
							Save Changes
						</Button>
					</div>
				</form>

				{/* Delete Account */}
				<section className="border-error/30 bg-error/5 rounded-2xl border p-6">
					<div className="flex items-start gap-4">
						<div className="bg-error/10 text-error flex h-10 w-10 items-center justify-center rounded-xl">
							<Trash2 size={20} />
						</div>

						<div className="flex-1">
							<h2 className="text-error font-semibold">Delete Account</h2>

							<p className="text-t-secondary mt-1 text-sm">
								Permanently remove your SignalOps account and all associated
								resources.
							</p>

							<div className="mt-6">
								<Button
									textColor="text-warning"
									loading={isDeleting}
									onClick={mutateDelete}
								>
									Delete Account
								</Button>
							</div>
						</div>
					</div>
				</section>
			</div>
		</Container>
	);
}

export default ProfilePage;
