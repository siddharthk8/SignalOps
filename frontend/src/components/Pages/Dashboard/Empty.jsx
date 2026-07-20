import { Activity } from "lucide-react";
import { useSelector } from "react-redux";

import Button from "@/components/Button";
import Container from "@/components/Container";

function EmptyDashboard({ onAction }) {
	const user = useSelector((state) => state.auth.user);

	return (
		<Container>
			<div className="flex min-h-[60vh] flex-col items-center justify-center px-6 text-center">
				<div className="bg-primary/10 text-primary flex size-16 items-center justify-center rounded-full">
					<Activity size={30} strokeWidth={2} />
				</div>

				<h1 className="text-t-primary mt-8 text-4xl font-bold tracking-tight">
					Welcome, {user.firstName}
				</h1>

				<p className="text-t-primary mt-3 text-lg font-medium">Your dashboard is ready.</p>

				<p className="text-t-muted mt-5 max-w-2xl text-sm leading-7">
					Connect your first source application to start monitoring incidents. Once data
					starts flowing, you'll see key metrics, trends, and recent activity here.
				</p>

				{onAction && (
					<div className="mt-8">
						<Button variant="success" onClick={onAction}>
							Create Source Application
						</Button>
					</div>
				)}
			</div>
		</Container>
	);
}

export default EmptyDashboard;
