import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { useNavigate } from "react-router";

import { createSourceApp } from "@/api";
import Container from "@/components/Container";
import FormPageHeader from "@/components/FormPageHeader";
import SourceAppForm from "@/components/Pages/CreateSourceApp/SourceAppForm";
import SourceAppPreview from "@/components/Pages/CreateSourceApp/SourceAppPreview";
import authenticatedClient from "@/core/api/customClient";
import { handleServerErrorOnMutate } from "@/shared/utils/handleServerErrorOnMutate";

export default function CreateSourceAppPage() {
	const navigate = useNavigate();
	const queryClient = useQueryClient();

	const [selectedType, setSelectedType] = useState("auth-app");

	const { mutate, isPending } = useMutation({
		mutationKey: ["create-source-app"],
		mutationFn: ({ appName, appType }) =>
			createSourceApp({
				client: authenticatedClient,
				body: {
					name: appName,
					app_type: appType,
				},
			}),
		onSuccess: ({ data }) => {
			queryClient.invalidateQueries({
				queryKey: ["source-apps"],
			});
			navigate(`/source-apps/${data.id}/batches`);
		},
	});

	const handleCreate = ({ appName, appType, setError }) => {
		mutate(
			{
				appName,
				appType,
			},
			{
				onError: (error) => {
					handleServerErrorOnMutate(error, setError);
				},
			},
		);
	};

	return (
		<Container className="space-y-8">
			<FormPageHeader
				title="Create Source Application"
				description="Register a new application to begin monitoring logs and detecting security incidents."
			/>

			<div className="grid gap-6 lg:grid-cols-[1.8fr_1fr]">
				<SourceAppForm
					isSubmitting={isPending}
					selectedType={selectedType}
					onTypeChange={setSelectedType}
					onSubmit={handleCreate}
				/>

				<SourceAppPreview appType={selectedType} />
			</div>
		</Container>
	);
}
