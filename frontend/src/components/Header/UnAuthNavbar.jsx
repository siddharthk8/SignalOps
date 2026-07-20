import { ArrowRight } from "lucide-react";
import { useLocation, useNavigate } from "react-router";

import Button from "../Button";

export default function UnauthNavbar() {
	const navigate = useNavigate();
	const location = useLocation();

	return (
		<>
			{location.pathname === "/login" ? (
				<Button
					onClick={() => navigate("/signup", { replace: true })} // This prevents unwanted loop from login to signup page and vice-versa.
					className="text-sm sm:text-base"
					variant="accent"
					rightIcon={<ArrowRight size={16} />}
				>
					Sign Up
				</Button>
			) : (
				!location.pathname.startsWith("/reset-password/") && (
					<Button
						onClick={() => {
							if (location.pathname == "/") {
								navigate("/login"); // This is important if navigating from homepage.
							} else {
								navigate("/login", { replace: true }); // This prevents unwanted loop from signup to login page and vice-versa.
							}
						}}
						variant="accent"
						className="text-sm sm:text-base"
						rightIcon={<ArrowRight size={16} />}
					>
						Log In
					</Button>
				)
			)}
		</>
	);
}
