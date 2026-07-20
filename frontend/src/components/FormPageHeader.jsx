import { ArrowLeft } from "lucide-react";
import { useNavigate } from "react-router";

import Button from "@/components/Button";

function FormPageHeader({
	title,
	description,
	backLabel = null, // Back
	onBack,
	actions,
	className = "",
}) {
	const navigate = useNavigate();

	const handleBack = () => {
		if (onBack) {
			onBack();
			return;
		}

		navigate(-1);
	};

	return (
		<section
			className={`flex flex-col gap-5 md:flex-row md:items-end md:justify-between ${className}`}
		>
			<div>
				{backLabel && (
					<div className="mb-3">
						<Button
							variant="ghost"
							leftIcon={<ArrowLeft size={16} />}
							onClick={handleBack}
						>
							{backLabel}
						</Button>
					</div>
				)}

				<h1 className="text-t-primary font-['Space_Grotesk'] text-3xl font-bold tracking-tight">
					{title}
				</h1>

				{description && (
					<p className="text-t-muted mt-2 max-w-2xl text-sm leading-6">{description}</p>
				)}
			</div>

			{actions && <div className="flex items-center gap-3">{actions}</div>}
		</section>
	);
}

export default FormPageHeader;
