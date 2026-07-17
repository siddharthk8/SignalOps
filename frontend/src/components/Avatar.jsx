export default function Avatar({ firstName, lastName, profileImage, size = "md" }) {
	const initials = `${firstName?.[0] || ""}${lastName?.[0] || ""}`.toUpperCase();

	const sizeClasses = {
		sm: "w-8 h-8 text-xs",
		md: "w-10 h-10 text-sm",
		lg: "w-14 h-14 text-base",
		xlg: "w-28 h-28 text-base",
	};

	const dimension = sizeClasses[size] || sizeClasses.md;

	if (profileImage) {
		return (
			<img
				src={profileImage}
				alt={`${firstName} ${lastName}`}
				className={`${dimension} border-border rounded-full border object-cover shadow-sm`}
			/>
		);
	}

	return (
		<div
			className={` ${dimension} bg-primary-200 text-primary-800 dark:bg-primary-400 dark:text-primary-900 border-border flex items-center justify-center rounded-full border font-semibold shadow-sm`}
		>
			{initials}
		</div>
	);
}
