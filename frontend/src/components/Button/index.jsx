import { Loader2 } from "lucide-react";

const variants = {
	primary:
		"bg-primary-500 text-white border-transparent shadow-sm hover:bg-primary-600 active:bg-primary-700",
	secondary:
		"bg-surface-tertiary text-t-primary border-transparent shadow-none hover:bg-surface-tertiary/70 active:bg-surface-tertiary",
	accent: "bg-accent-500 text-white border-transparent shadow-sm hover:bg-accent-600 active:bg-accent-700",
	success:
		"bg-success/10 text-success border-success/25 hover:bg-success/20 active:bg-success/25",
	danger: "bg-error/10 text-error border-error/25 hover:bg-error/20 active:bg-error/25",
	warning:
		"bg-warning/10 text-warning border-warning/25 hover:bg-warning/20 active:bg-warning/25",
	outline:
		"bg-transparent text-t-primary border-border shadow-none hover:border-primary/50 hover:bg-primary/5 active:bg-primary/10",
	ghost: "bg-transparent text-t-primary border-transparent shadow-none hover:bg-surface-secondary active:bg-surface-tertiary",
	link: "bg-transparent text-primary-500 border-transparent shadow-none hover:text-primary-600 hover:underline underline-offset-4 active:text-primary-700",
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
			className={`group focus-visible:ring-primary/30 relative inline-flex cursor-pointer items-center justify-center overflow-hidden border border-black/10 font-medium shadow-sm transition-colors duration-200 focus-visible:ring-2 focus-visible:outline-none active:opacity-95 disabled:pointer-events-none disabled:opacity-60 dark:border-white/10 dark:hover:border-white/15 ${sizes[size]} ${variants[variant]} ${className}`}
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
