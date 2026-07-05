const FormField = ({ label = null, labelId = undefined, error, children, className = "" }) => {
	return (
		<div className={`flex flex-col gap-1 py-1 ${className}`}>
			{label && (
				<label htmlFor={labelId} className="text-sm font-medium text-t-secondary">
					{label}
				</label>
			)}

			{children}

			{error && <p className="text-xs text-error mt-1">{error}</p>}
		</div>
	);
};

export default FormField;
