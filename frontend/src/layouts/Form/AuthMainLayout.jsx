import FormSide from "./FormSideLayout";

export default function AuthMainLayout({
	imageSrc,
	title,
	description,
	headerText,
	headerContent,
	children,
}) {
	return (
		<div className="min-h-full grid grid-cols-1 lg:grid-cols-2 bg-bg">
			<div className="hidden lg:block relative overflow-hidden border-r border-border">
				{/* Background image */}
				<img
					// src="none"
					src={imageSrc}
					alt="Brand background"
					className="absolute inset-0 h-full w-full object-cover"
				/>

				<div className="absolute inset-0 bg-linear-to-t from-black/60 via-black/20 to-transparent" />

				<div className="relative z-10 flex h-full items-end p-12">
					<div className="max-w-md">
						<h2 className="text-4xl font-semibold leading-tight text-white mb-3 drop-shadow-lg">
							{title}
						</h2>

						<p className="text-sm text-white/90 leading-relaxed drop-shadow">
							{description}
						</p>
					</div>
				</div>
			</div>

			<FormSide headerText={headerText} headerContent={headerContent}>
				{children}
			</FormSide>
		</div>
	);
}
