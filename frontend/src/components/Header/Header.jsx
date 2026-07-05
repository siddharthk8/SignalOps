import { useSelector } from "react-redux";

import Navbar from "./Navbar";

function Header() {
	const auth = useSelector((state) => state.auth);

	return (
		<header className="z-100">
			<Navbar auth={auth} />
		</header>
	);
}

export default Header;
