import { Eye, EyeOff } from "lucide-react";
import { useState } from "react";

import Input from "./Input";

const PasswordInput = ({ ...props }) => {
	const [visible, setVisible] = useState(false);

	return (
		<Input
			{...props}
			type={visible ? "text" : "password"}
			autoComplete="off"
			rightIcon={
				<button
					type="button"
					onClick={() => setVisible((v) => !v)}
					className="text-t-muted hover:text-t-primary transition-colors"
					aria-label={visible ? "Hide password" : "Show password"}
					tabIndex={-1}
				>
					{visible ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
				</button>
			}
		/>
	);
};

export default PasswordInput;
