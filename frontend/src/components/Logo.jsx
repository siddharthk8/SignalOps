import { SparklesIcon } from "lucide-react";

export default function Logo({ className = "", ...props }) {
	return <SparklesIcon className={`size-5 ${className}`} {...props} />;
}
