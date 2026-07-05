import { ChevronDown } from "lucide-react";
import { useId } from "react";

import FormField from "./FormField";

/*
Usage Example :-

  useForm({
    mode: "onBlur",
    defaultValues: {
      FIELD_NAME: "",
      // ... we don't have to provide defaultValues for other fields in the form.
    },
  });

  +

  <SelectInput
    label="Role"
    autoComplete="off"
    {...register("FIELD_NAME", {
      required: "Role is required",
    })}
    error={errors.FIELD_NAME?.message}
  >
    <option value="" disabled hidden>
      Select a FIELD_NAME
    </option>
    <option value="admin">Administrator</option>
    <option value="editor">Editor</option>
    <option value="viewer">Viewer</option>
  </SelectInput>
*/

const SelectInput = ({
	label,
	error,
	autoComplete = "off",
	className = "",
	disabled = false,
	children,
	...props
}) => {
	const id = useId();

	return (
		<FormField label={label} error={error} labelId={id}>
			<div className="relative">
				<select
					id={id}
					disabled={disabled}
					autoComplete={autoComplete}
					className={`
            w-full appearance-none rounded-md border px-3 py-2 pr-10 text-sm
            bg-surface text-t-primary
            border-border shadow-sm
            transition-colors duration-200
            focus:outline-none focus:ring-2

            ${
				error
					? "border-error focus:ring-error"
					: "focus:border-primary focus:ring-primary-300"
			}

            ${disabled ? "bg-elevated text-t-disabled cursor-not-allowed opacity-70" : ""}

            ${className}
          `}
					{...props}
				>
					{children}
				</select>

				{/* Chevron */}
				<ChevronDown
					className="
            pointer-events-none absolute right-3 top-1/2 h-4 w-4
            -translate-y-1/2 text-t-muted
          "
				/>
			</div>
		</FormField>
	);
};

export default SelectInput;
