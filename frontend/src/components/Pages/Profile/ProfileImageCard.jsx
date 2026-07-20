import { useMutation } from "@tanstack/react-query";
import { useDispatch } from "react-redux";

import { deleteProfileImage, uploadProfileImage } from "@/api";
import ProfileImagePicker from "@/components/Input/ProfileImagePicker";
import authenticatedClient from "@/core/api/customClient";
import { handleServerErrorOnMutate } from "@/shared/utils/handleServerErrorOnMutate";
import { updateProfileImage } from "@/store/features/authSlice";

function ProfileImageCard({ setError, clearErrors, value, setSuccess }) {
	const dispatch = useDispatch();

	const { mutate, isPending } = useMutation({
		mutationFn: (profileImage) => {
			if (!profileImage) {
				return deleteProfileImage({
					client: authenticatedClient,
				});
			}
			return uploadProfileImage({
				client: authenticatedClient,
				body: {
					file: profileImage,
				},
			});
		},
		onSuccess: ({ data }) => {
			dispatch(updateProfileImage(data.profile_image_path || null)); // This null statement is very important otherwise changes do not reflect properly.
			setSuccess(true);
		},
		onError: (error) => {
			handleServerErrorOnMutate(error, setError);
		},
	});

	const handleChange = (profileImage) => {
		clearErrors("root");
		setSuccess(false);
		mutate(profileImage);
	};

	return (
		<div className="border-border mb-8 border-b pb-8">
			<ProfileImagePicker value={value} loading={isPending} onChange={handleChange} />
		</div>
	);
}

export default ProfileImageCard;
