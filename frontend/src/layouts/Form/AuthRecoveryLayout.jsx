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
		<div className="bg-bg grid min-h-full grid-cols-1 lg:grid-cols-2">
			<div className="relative m-16 mr-0 hidden overflow-hidden lg:block">
				{/* Background image */}
				<img
					// src="none"
					src={imageSrc}
					alt="Brand background"
					className="absolute inset-0 h-full w-full rounded-2xl object-cover"
				/>

				<div className="absolute inset-0 rounded-2xl bg-black/40" />

				<div className="relative z-10 flex h-full flex-col justify-center px-8 sm:px-12 lg:px-16">
					<h2 className="mb-4 text-4xl leading-tight font-bold text-white drop-shadow-md">
						{title}
					</h2>
					<p className="text-lg leading-relaxed text-white/90 drop-shadow">
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
