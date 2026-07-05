import { Link } from "react-router";

const FormBottomLink = ({
	text,
	linkTextOrComp, // This could aslo be a component
	to = "", // Optional
	className = "",
}) => {
	return (
		<p className={`text-sm text-t-muted text-center ${className}`}>
			{text}{" "}
			<Link
				to={to}
				className="text-primary font-medium hover:underline transition-colors cursor-pointer duration-200"
			>
				{linkTextOrComp}
			</Link>
		</p>
	);
};

export default FormBottomLink;
