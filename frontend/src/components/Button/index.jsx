export default function Button({
	children = "Button",
	buttonColor = "bg-primary",
	textColor = "text-t-primary",
	className = "",
	...props
}) {
	return (
		<button
			className={`group relative inline-flex items-center justify-center overflow-hidden rounded-lg border border-border bg-surface px-3 py-1.5 text-sm ${textColor} transition-all duration-300 ease-out hover:-translate-y-0.5 hover:border-primary hover:shadow-sm active:translate-y-0 active:scale-[0.98] focus:outline-none focus:ring-2 focus:ring-primary/20 ${className}`}
			{...props}
		>
			<div
				className={`absolute left-0 top-0 h-full w-1 ${buttonColor} transition-all duration-300 group-hover:w-1.5`}
			/>

			<div className="absolute inset-0 bg-linear-to-r from-white/5 via-transparent to-transparent opacity-0 transition-opacity duration-300 group-hover:opacity-100" />

			<div className="relative z-10 flex items-center gap-2.5">
				{/* Status Dot */}
				<div
					className={`h-2 w-2 rounded-full ${buttonColor} transition-all duration-300 group-hover:scale-125`}
				/>

				{/* Label */}
				<span className="font-medium whitespace-nowrap">{children}</span>

				{/* Arrow */}
				<svg
					className="h-4 w-4 translate-x-0 opacity-0 transition-all duration-300 group-hover:translate-x-1 group-hover:opacity-100"
					viewBox="0 0 24 24"
					fill="none"
					stroke="currentColor"
					strokeWidth="2"
					strokeLinecap="round"
					strokeLinejoin="round"
				>
					<path d="M5 12h14" />
					<path d="M13 5l7 7-7 7" />
				</svg>
			</div>
		</button>
	);
}
