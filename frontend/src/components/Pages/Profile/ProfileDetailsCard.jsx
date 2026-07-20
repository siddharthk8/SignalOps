import { useMutation } from "@tanstack/react-query";
import { useEffect, useState } from "react";
import { Controller, useForm } from "react-hook-form";
import { useDispatch } from "react-redux";

import { updateCurrentUser } from "@/api";
import Button from "@/components/Button";
import FormMessage from "@/components/Form/FormMessage";
import Input from "@/components/Input/Input";
import authenticatedClient from "@/core/api/customClient";
import {
	FIRST_NAME_RULES_NRQ,
	LAST_NAME_RULES_NRQ,
} from "@/shared/constants/HookFormValidatonRules";
import { FormStyle } from "@/shared/constants/Styles";
import { handleServerErrorOnMutate } from "@/shared/utils/handleServerErrorOnMutate";
import { updateNames } from "@/store/features/authSlice";

import ProfileImageCard from "./ProfileImageCard";

function ProfileDetailsCard({ user }) {
	const dispatch = useDispatch();
	const [success, setSuccess] = useState(false);

	const {
		register,
		handleSubmit,
		control,
		setError,
		clearErrors,
		reset,
		watch,
		formState: { errors, isDirty },
	} = useForm({
		mode: "onBlur",
		defaultValues: {
			firstName: user.firstName,
			lastName: user.lastName,
			profileImage: user.profileImage,
		},
	});

	useEffect(() => {
		reset({
			firstName: user.firstName,
			lastName: user.lastName,
			profileImage: user.profileImage,
		});
	}, [user.firstName, user.lastName, user.profileImage, reset]);

	watch(); // It is required here to ensure isDirty updates correctly.

	const { mutate: updateProfile, isPending: isUpdating } = useMutation({
		mutationFn: ({ firstName, lastName }) =>
			updateCurrentUser({
				client: authenticatedClient,
				body: {
					first_name: firstName,
					last_name: lastName,
				},
			}),
		onSuccess: ({ data }) => {
			dispatch(
				updateNames({
					firstName: data.first_name,
					lastName: data.last_name,
				}),
			);
			setSuccess(true);
		},
		onError: (error) => {
			handleServerErrorOnMutate(error, setError);
		},
	});

	const submit = ({ firstName, lastName }) => {
		clearErrors("root");
		setSuccess(false);

		updateProfile({
			firstName,
			lastName,
		});
	};

	return (
		<section className="border-border bg-surface rounded-lg border">
			<div className="border-border border-b px-6 py-5">
				<h2 className="text-t-primary text-lg font-semibold">Personal Information</h2>

				<p className="text-t-muted mt-1 text-sm">
					Update your account information and profile photo.
				</p>
			</div>

			<form onSubmit={handleSubmit(submit)} noValidate className={`${FormStyle} border-0`}>
				<FormMessage message={errors.root?.message} />

				{success && (
					<FormMessage
						type="success"
						message="Your profile has been updated successfully."
					/>
				)}

				<Controller
					name="profileImage"
					control={control}
					render={({ field: { value } }) => (
						<ProfileImageCard
							setError={setError}
							clearErrors={clearErrors}
							value={value}
							setSuccess={setSuccess}
						/>
					)}
				/>

				<div className="grid gap-5 md:grid-cols-2">
					<Input
						label="First Name"
						placeholder="Enter first name"
						error={errors.firstName?.message}
						{...register("firstName", FIRST_NAME_RULES_NRQ)}
					/>

					<Input
						label="Last Name"
						placeholder="Enter last name"
						error={errors.lastName?.message}
						{...register("lastName", LAST_NAME_RULES_NRQ)}
					/>
				</div>

				<Input label="Email Address" type="email" value={user.email} disabled />

				<div className="border-border flex justify-end border-t pt-6">
					<Button
						type="submit"
						loading={isUpdating}
						loadingText="Saving..."
						disabled={!isDirty || isUpdating}
					>
						Save Changes
					</Button>
				</div>
			</form>
		</section>
	);
}

export default ProfileDetailsCard;
