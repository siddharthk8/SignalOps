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
		<div className="bg-bg grid min-h-full grid-cols-1 lg:grid-cols-2">
			<div className="border-border relative hidden overflow-hidden border-r lg:block">
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
						<h2 className="mb-3 text-4xl leading-tight font-semibold text-white drop-shadow-lg">
							{title}
						</h2>

						<p className="text-sm leading-relaxed text-white/90 drop-shadow">
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
