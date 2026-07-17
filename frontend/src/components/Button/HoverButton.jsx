function HoverButton({ children, className = "", ...props }) {
	return (
		<button
			aria-haspopup="true"
			className={`hover:bg-elevated rounded-lg p-1.5 transition sm:p-2 ${className}`}
			{...props}
		>
			{children}
		</button>
	);
}

export default HoverButton;
