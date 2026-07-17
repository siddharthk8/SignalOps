import { Link } from "react-router";

const FormBottomLink = ({
	text,
	linkTextOrComp, // This could aslo be a component
	to = "", // Optional
	className = "",
}) => {
	return (
		<p className={`text-t-muted text-center text-sm ${className}`}>
			{text}{" "}
			<Link
				to={to}
				className="text-primary cursor-pointer font-medium transition-colors duration-200 hover:underline"
			>
				{linkTextOrComp}
			</Link>
		</p>
	);
};

export default FormBottomLink;
