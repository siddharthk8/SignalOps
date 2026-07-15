import { useEffect } from "react";
import { useLocation } from "react-router";

import ArchitectureSection from "@/components/Pages/Landing/Architecture";
import BottomSection from "@/components/Pages/Landing/Bottom";
import FeaturesSection from "@/components/Pages/Landing/Features";
import HeroSection from "@/components/Pages/Landing/Hero";
import PhilosophySection from "@/components/Pages/Landing/Philosophy";
import TechStackSection from "@/components/Pages/Landing/TechStack";
import WorkflowSection from "@/components/Pages/Landing/Workflow";

function App() {
	const location = useLocation();

	useEffect(() => {
		if (!location.hash) return;

		const element = document.querySelector(location.hash);

		if (element) {
			element.scrollIntoView({
				behavior: "smooth",
			});
		}
	}, [location]);

	return (
		<div>
			<HeroSection />
			<PhilosophySection />
			<FeaturesSection />
			<ArchitectureSection />
			<WorkflowSection />
			<TechStackSection />
			<BottomSection />
		</div>
	);
}

export default App;
