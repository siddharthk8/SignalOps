import { useId } from "react";
import { Link } from "react-router";

import FormField from "./FormField";

const Checkbox = ({ label, error, className = "", disabled = false, link, ...props }) => {
	const id = useId();

	return (
		<FormField error={error} className={className}>
			<label
				htmlFor={id}
				className={`
					flex items-start gap-3 text-sm text-t-secondary
					${disabled ? "opacity-70 cursor-not-allowed" : "cursor-pointer"}
				`}
			>
				<input
					id={id}
					type="checkbox"
					disabled={disabled}
					className={`
						h-4 w-4 my-auto
						accent-primary-400
						border-border
						focus:ring-2 focus:ring-primary-300
						transition-colors
					`}
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
