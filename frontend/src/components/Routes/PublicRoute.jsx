import { useSelector } from "react-redux";
import { Navigate, Outlet } from "react-router";

function PublicRoute() {
	const user = useSelector((state) => state.auth.user);

	if (user) {
		return <Navigate to="/dashboard" replace />;
	}

	return <Outlet />;
}

export default PublicRoute;
