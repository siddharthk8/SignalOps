import { useMutation } from "@tanstack/react-query";
import { AlertTriangle, Trash2 } from "lucide-react";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { useDispatch } from "react-redux";

import { deleteCurrentUser } from "@/api";
import Button from "@/components/Button";
import FormMessage from "@/components/Form/FormMessage";
import authenticatedClient from "@/core/api/customClient";
import { clearUser } from "@/store/features/authSlice";

function DeleteAccountCard({ handleServerErrorOnMutate }) {
	const dispatch = useDispatch();

	const [confirming, setConfirming] = useState(false);

	const {
		setError,
		clearErrors,
		formState: { errors },
	} = useForm();

	const { mutate, isPending } = useMutation({
		mutationFn: () =>
			deleteCurrentUser({
				client: authenticatedClient,
			}),
		onSuccess: () => {
			dispatch(clearUser());
		},
		onError: (error) => {
			handleServerErrorOnMutate(error, setError);
		},
	});

	const handleDelete = () => {
		clearErrors("root");

		if (!confirming) {
			setConfirming(true);
			return;
		}
		mutate();
	};

	return (
		<section className="border-error/30 bg-error/5 rounded-lg border p-6">
			<div className="flex items-start gap-4">
				<div className="bg-error/10 text-error flex size-11 shrink-0 items-center justify-center rounded-lg">
					<Trash2 size={20} />
				</div>

				<div className="flex-1">
					<h2 className="text-error font-semibold">Delete Account</h2>

					<p className="text-t-secondary mt-1 text-sm leading-6">
						Permanently remove your account and all associated resources. This action
						cannot be undone.
					</p>

					<FormMessage message={errors.root?.message} />

					{confirming && (
						<div className="border-error/20 bg-error/10 mt-5 flex gap-3 rounded-md border p-4">
							<AlertTriangle className="text-error mt-0.5 shrink-0" size={18} />

							<div>
								<p className="text-t-primary text-sm font-medium">
									Are you sure you want to delete your account?
								</p>

								<p className="text-t-muted mt-1 text-xs leading-5">
									This will permanently delete your profile, settings, and all
									associated data. This action cannot be undone.
								</p>
							</div>
						</div>
					)}

					<div className="mt-6 flex gap-3">
						<Button
							loading={isPending}
							loadingText="Deleting..."
							onClick={handleDelete}
						>
							{confirming ? "Confirm Delete" : "Delete Account"}
						</Button>

						{confirming && (
							<Button
								variant="secondary"
								disabled={isPending}
								onClick={() => {
									clearErrors("root");
									setConfirming(false);
								}}
							>
								Cancel
							</Button>
						)}
					</div>
				</div>
			</div>
		</section>
	);
}

export default DeleteAccountCard;
