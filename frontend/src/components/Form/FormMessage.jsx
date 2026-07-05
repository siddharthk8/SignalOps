const FORM_MESSAGE_VARIANT_STYLES = {
	error: "border-error text-error",
	success: "border-success text-success",
	warning: "border-warning text-warning",
	info: "border-info text-info",
};

const FormMessage = ({ message, type = "error", className = "" }) => {
	if (!message) return null;

	return (
		<div
			role="alert"
			className={`mb-4 rounded-md border px-4 py-2 text-sm ${FORM_MESSAGE_VARIANT_STYLES[type]} ${className}`}
		>
			{message}
		</div>
	);
};

export default FormMessage;
