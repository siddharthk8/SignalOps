function FormSide({ headerText, headerContent, children }) {
	return (
		<div className="flex items-center justify-center px-6 py-8">
			<div className="w-full max-w-md">
				{headerText && headerContent && (
					<div className="mb-6">
						<h1 className="text-t-primary mb-1 text-2xl font-semibold">{headerText}</h1>
						<p className="text-t-muted text-sm">{headerContent}</p>
					</div>
				)}

				{children}
			</div>
		</div>
	);
}

export default FormSide;
