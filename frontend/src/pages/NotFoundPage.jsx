import Container from "@/components/Container";

function NotFoundPage() {
	return (
		<div className="bg-bg flex items-center justify-center">
			<Container>
				<div className="mx-auto max-w-xl text-center">
					<p className="font-dancing text-primary/20 text-9xl font-bold select-none">
						404
					</p>

					<h1 className="text-t-primary mt-2 text-4xl font-bold">Oops! Page not found</h1>
					<p className="text-t-muted mx-auto mt-4 max-w-md text-lg">
						The page you're looking for doesn't exist, may have been moved, or the URL
						might be incorrect.
					</p>
				</div>
			</Container>
		</div>
	);
}

export default NotFoundPage;
