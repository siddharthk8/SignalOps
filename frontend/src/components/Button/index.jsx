import { ArrowRight, LoaderCircle } from "lucide-react";
import { forwardRef } from "react";

const Button = forwardRef(function Button(
	{
		children,
		type = "button",

		// Appearance
		buttonColor = "bg-primary",
		textColor = "text-t-primary",
		className = "",

		// State
		loading = false,
		loadingText = "Loading...",
		disabled = false,

		// Icons
		leftIcon = null,
		rightIcon = <ArrowRight className="h-4 w-4" />,

		...props
	},
	ref,
) {
	const isDisabled = disabled || loading;

	return (
		<button
			ref={ref}
			type={type}
			disabled={isDisabled}
			aria-disabled={isDisabled}
			aria-busy={loading}
			className={`group border-border bg-surface relative inline-flex items-center justify-center overflow-hidden rounded-lg border px-3 py-2 text-sm font-medium select-none ${textColor} focus:ring-primary/20 transition-all duration-300 focus:ring-2 focus:outline-none ${
				loading
					? "cursor-wait opacity-70"
					: disabled
						? "cursor-not-allowed opacity-60"
						: "hover:border-primary hover:-translate-y-0.5 hover:shadow-md active:translate-y-0 active:scale-[0.98]"
			} ${className} `}
			{...props}
		>
			{/* Left Accent */}
			<div
				className={`absolute top-0 left-0 h-full w-1 ${buttonColor} transition-all duration-300 ${!isDisabled ? "group-hover:w-1.5" : ""} `}
			/>

			{/* Shine */}
			{!isDisabled && (
				<div className="absolute inset-0 bg-linear-to-r from-white/5 via-transparent to-transparent opacity-0 transition-opacity duration-300 group-hover:opacity-100" />
			)}

			<div className="relative z-10 flex items-center gap-2">
				{/* Left Icon / Spinner / Status Dot */}
				{loading ? (
					<LoaderCircle className="h-[18px] w-[18px] shrink-0 animate-spin" />
				) : leftIcon ? (
					<span className="shrink-0">{leftIcon}</span>
				) : (
					<div
						className={`h-2 w-2 shrink-0 rounded-full ${buttonColor} transition-transform duration-300 ${!isDisabled ? "group-hover:scale-125" : ""} `}
					/>
				)}

				{/* Text */}
				<span className="whitespace-nowrap">{loading ? loadingText : children}</span>

				{/* Right Icon */}
				{!loading && rightIcon && (
					<span
						className={`shrink-0 transition-all duration-300 ${
							isDisabled
								? "opacity-40"
								: "translate-x-0 opacity-0 group-hover:translate-x-1 group-hover:opacity-100"
						} `}
					>
						{rightIcon}
					</span>
				)}
			</div>
		</button>
	);
});

Button.displayName = "Button";

export default Button;
