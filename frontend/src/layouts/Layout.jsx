import { Outlet, ScrollRestoration } from "react-router";

import Footer from "../components/Footer/Footer";
import Header from "../components/Header/Header";

const Layout = () => {
	return (
		<div className="bg-bg text-t-primary flex h-screen w-full flex-col">
			<Header />
			{/* Below margin-top values are related to navbar height */}
			<main className="mt-[57px] flex flex-1 flex-row sm:mt-[65px]">
				<div className="w-full">
					<Outlet />
				</div>
			</main>
			<Footer />

			<ScrollRestoration />
		</div>
	);
};

export default Layout;
