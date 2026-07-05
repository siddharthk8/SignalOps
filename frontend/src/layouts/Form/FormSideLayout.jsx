function FormSide({ headerText, headerContent, children }) {
	return (
		<div className="flex py-8 items-center justify-center px-6">
			<div className="w-full max-w-md">
				{headerText && headerContent && (
					<div className="mb-6">
						<h1 className="text-2xl font-semibold text-t-primary mb-1">{headerText}</h1>
						<p className="text-sm text-t-muted">{headerContent}</p>
					</div>
				)}

				{children}
			</div>
		</div>
	);
}

export default FormSide;
