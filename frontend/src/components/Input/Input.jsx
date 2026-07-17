import { useId } from "react";

import FormField from "./FormField";

const Input = ({
	label,
	error,
	rightIcon = null,
	autoComplete = "off",
	className = "",
	type = "text",
	disabled = false,
	...props
}) => {
	const id = useId();

	return (
		<FormField label={label} error={error} labelId={id}>
			<div className="relative">
				<input
					id={id}
					type={type}
					disabled={disabled}
					autoComplete={autoComplete}
					className={`bg-surface text-t-primary border-border w-full rounded-md border px-3 py-2 text-sm shadow-sm transition-colors duration-200 focus:ring-2 focus:outline-none ${error ? "border-error focus:ring-error" : "focus:border-primary focus:ring-primary-300"} ${disabled ? "bg-elevated text-t-disabled cursor-not-allowed opacity-70" : ""} ${rightIcon ? "pr-10" : ""} placeholder:text-t-muted ${className} `}
					{...props}
				/>

				{rightIcon && (
					<div className="text-t-muted absolute inset-y-0 right-3 flex items-center">
						{rightIcon}
					</div>
				)}
			</div>
		</FormField>
	);
};

export default Input;
