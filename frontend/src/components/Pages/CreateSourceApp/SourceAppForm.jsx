import { ArrowRight } from "lucide-react";
import { useForm } from "react-hook-form";

import Button from "@/components/Button";
import FormMessage from "@/components/Form/FormMessage";
import Input from "@/components/Input/Input";
import SelectInput from "@/components/Input/SelectInput";
import { APP_NAME_RULES } from "@/shared/constants/HookFormValidatonRules";

function SourceAppForm({ isSubmitting, selectedType, onTypeChange, onSubmit }) {
	const {
		register,
		handleSubmit,
		setError,
		clearErrors,
		formState: { errors },
	} = useForm({
		mode: "onBlur",
		defaultValues: {
			appName: "",
			appType: selectedType,
		},
	});

	const submit = ({ appName, appType }) => {
		clearErrors("root");

		onSubmit({
			appName,
			appType,
			setError,
		});
	};

	return (
		<section className="border-border bg-surface overflow-hidden rounded-lg border">
			<div className="border-border border-b px-6 py-5">
				<h2 className="text-t-primary text-lg font-semibold">Application Details</h2>

				<p className="text-t-muted mt-1 text-sm">
					Configure the basic information for your source application.
				</p>
			</div>

			<form onSubmit={handleSubmit(submit)} noValidate className="space-y-8 p-6">
				<FormMessage message={errors.root?.message} />

				{/* Name */}
				<div>
					<div className="mb-4 flex items-center gap-3">
						<div className="bg-primary/10 text-primary flex h-7 w-7 items-center justify-center rounded-md text-xs font-semibold">
							01
						</div>

						<div>
							<h3 className="text-t-primary text-sm font-medium">Application Name</h3>

							<p className="text-t-muted text-xs">Choose a descriptive name.</p>
						</div>
					</div>

					<Input
						placeholder="e.g. Authentication Service"
						error={errors.appName?.message}
						{...register("appName", APP_NAME_RULES)}
					/>
				</div>

				{/* Type */}
				<div>
					<div className="mb-4 flex items-center gap-3">
						<div className="bg-primary/10 text-primary flex h-7 w-7 items-center justify-center rounded-md text-xs font-semibold">
							02
						</div>

						<div>
							<h3 className="text-t-primary text-sm font-medium">Application Type</h3>

							<p className="text-t-muted text-xs">This helps categorize incidents.</p>
						</div>
					</div>

					<SelectInput
						error={errors.appType?.message}
						{...register("appType", {
							required: "Application type is required",
							onChange: (e) => onTypeChange(e.target.value),
						})}
					>
						<option value="auth-app">Authentication</option>
						<option value="payment-app">Payment</option>
						<option value="order-app">Order</option>
					</SelectInput>
				</div>

				<div className="border-border -mx-6 -mb-6 flex items-center justify-end border-t px-6 py-5">
					<Button
						type="submit"
						loading={isSubmitting}
						rightIcon={<ArrowRight size={16} />}
						loadingText="Creating..."
					>
						Create & Continue
					</Button>
				</div>
			</form>
		</section>
	);
}

export default SourceAppForm;
