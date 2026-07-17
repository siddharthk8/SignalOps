const FormField = ({ label = null, labelId = undefined, error, children, className = "" }) => {
	return (
		<div className={`flex flex-col gap-1 py-1 ${className}`}>
			{label && (
				<label htmlFor={labelId} className="text-t-secondary text-sm font-medium">
					{label}
				</label>
			)}

			{children}

			{error && <p className="text-error mt-1 text-xs">{error}</p>}
		</div>
	);
};

export default FormField;
