import FormSide from "./FormSideLayout";

export default function AuthRecoveryLayout({
	imageSrc,
	title,
	description,
	headerText,
	headerContent,
	children,
}) {
	return (
		<div className="min-h-full grid grid-cols-1 lg:grid-cols-2 bg-bg">
			<div className="hidden lg:block relative overflow-hidden m-16 mr-0">
				{/* Background image */}
				<img
					// src="none"
					src={imageSrc}
					alt="Brand background"
					className="absolute inset-0 h-full w-full object-cover rounded-2xl"
				/>

				<div className="absolute inset-0 bg-black/40 rounded-2xl" />

				<div className="relative z-10 flex flex-col justify-center h-full px-8 sm:px-12 lg:px-16">
					<h2 className="text-4xl font-bold text-white mb-4 leading-tight drop-shadow-md">
						{title}
					</h2>
					<p className="text-lg text-white/90 leading-relaxed drop-shadow">
						{description}
					</p>
				</div>
			</div>

			<FormSide headerText={headerText} headerContent={headerContent}>
				{children}
			</FormSide>
		</div>
	);
}
