import { useId } from "react";
import { Link } from "react-router";

import FormField from "./FormField";

const Checkbox = ({ label, error, className = "", disabled = false, link, ...props }) => {
	const id = useId();

	return (
		<FormField error={error} className={className}>
			<label
				htmlFor={id}
				className={`text-t-secondary flex items-start gap-3 text-sm ${disabled ? "cursor-not-allowed opacity-70" : "cursor-pointer"} `}
			>
				<input
					id={id}
					type="checkbox"
					disabled={disabled}
					className={`accent-primary-400 border-border focus:ring-primary-300 my-auto h-4 w-4 transition-colors focus:ring-2`}
					{...props}
				/>

				<span>
					{label}{" "}
					{link && (
						<Link
							to={link.href}
							className="text-primary hover:underline"
							onClick={(e) => e.stopPropagation()}
						>
							{link.text}
						</Link>
					)}
				</span>
			</label>
		</FormField>
	);
};

export default Checkbox;
