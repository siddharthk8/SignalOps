export default function Logo({ className = "" }) {
	return (
		<div className={className}>
			<img
				src="/favicon.svg"
				alt="Logo"
				className="h-full w-full scale-[2.5] object-contain"
			/>
		</div>
	);
}
