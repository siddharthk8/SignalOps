import { Loader2 } from "lucide-react";

const variants = {
	primary: "bg-primary-200 text-t-primary hover:bg-primary-400/80",
	success: "bg-success/15 text-success hover:bg-success/25",
	danger: "bg-error/15 text-error hover:bg-error/25",
	warning: "bg-warning/15 text-warning hover:bg-warning/25",
	secondary: "bg-surface-secondary text-t-primary hover:bg-surface-tertiary",
	ghost: "bg-transparent text-t-primary hover:bg-surface-secondary",
};

const sizes = {
	sm: "h-8 px-3 text-xs gap-1.5 rounded-md",
	md: "h-10 px-5 text-sm gap-2 rounded-lg",
	lg: "h-12 px-6 text-base gap-2.5 rounded-xl",
};

export default function Button({
	children,
	type = "button",
	variant = "primary",
	size = "md",
	className = "",
	loading = false,
	loadingText = "Loading...",
	disabled = false,
	leftIcon = null,
	rightIcon = null,
	...props
}) {
	return (
		<button
			type={type}
			disabled={disabled || loading}
			className={`group focus-visible:ring-primary/30 relative inline-flex items-center justify-center overflow-hidden border border-black/10 font-medium shadow-sm transition-colors duration-200 focus-visible:ring-2 focus-visible:outline-none active:opacity-95 disabled:pointer-events-none disabled:opacity-60 dark:border-white/10 dark:hover:border-white/15 ${sizes[size]} ${variants[variant]} ${className}`}
			{...props}
		>
			{loading ? (
				<>
					<Loader2 className="h-4 w-4 animate-spin" />
					<span>{loadingText}</span>
				</>
			) : (
				<>
					{leftIcon && <span>{leftIcon}</span>}
					<span>{children}</span>
					{rightIcon && <span>{rightIcon}</span>}
				</>
			)}
		</button>
	);
}
