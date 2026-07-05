import { useEffect } from "react";
import { useLocation } from "react-router";

function App() {
	const location = useLocation();

	useEffect(() => {
		if (!location.hash) return;

		const element = document.querySelector(location.hash);
		if (element) {
			element.scrollIntoView({ behavior: "smooth" });
		}
	}, [location]);

	return (
		<div className="flex flex-1 flex-col">
			<div id="overview" className="min-h-screen w-full bg-green-800"></div>
			<div id="pipeline" className="min-h-screen w-full bg-cyan-800"></div>
			<div id="features" className="min-h-screen w-full bg-blue-800"></div>
			<div id="architecture" className="min-h-screen w-full bg-amber-700"></div>
			<div id="demo" className="min-h-screen w-full bg-amber-900"></div>
		</div>
	);
}

export default App;
