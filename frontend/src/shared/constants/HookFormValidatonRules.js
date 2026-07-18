const TRIM_RULE = {
	setValueAs: (value) => (typeof value === "string" ? value.trim() : value),
};

export const EMAIL_RULES = {
	required: "Email is required",
	setValueAs: (value) => (typeof value === "string" ? value.trim().toLowerCase() : value), // Normalize email before returning to onSubmitHandler.
	pattern: {
		value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
		message: "Enter a valid email address",
	},
	maxLength: {
		value: 254, // RFC 5321 limit
		message: "Email is too long",
	},
};

export const PASSWORD_RULES = {
	required: "Password is required",
	minLength: {
		value: 8,
		message: "Password must be at least 8 characters",
	},
	maxLength: {
		value: 50,
		message: "Password is too long",
	},
	validate: {
		// Prevent whitespace-only passwords
		notEmpty: (value) => value.trim().length > 0 || "Password cannot be empty",
		strongPassword: (value) =>
			(/[A-Za-z]/.test(value) && /[^\w\s]/.test(value) && /\d/.test(value)) ||
			"Password must include letter, special character and a number",
	},
};

export const FIRST_NAME_RULES_NRQ = {
	...TRIM_RULE,
	minLength: {
		value: 2,
		message: "First name is too short",
	},
	maxLength: {
		value: 60,
		message: "First name is too long",
	},
};

export const LAST_NAME_RULES_NRQ = {
	...TRIM_RULE,
	minLength: {
		value: 2,
		message: "Last name is too short",
	},
	maxLength: {
		value: 80,
		message: "Last name is too long",
	},
};

export const FIRST_NAME_RULES = {
	...FIRST_NAME_RULES_NRQ,
	required: "First name is required",
};

export const LAST_NAME_RULES = {
	...LAST_NAME_RULES_NRQ,
	required: "Last name is required",
};

export const APP_NAME_RULES = {
	...TRIM_RULE,
	required: "Application name is required",
	minLength: {
		value: 2,
		message: "Application name is too short",
	},
	maxLength: {
		value: 50,
		message: "Application name is too long",
	},
};
