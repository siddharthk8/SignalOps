import Container from "@/components/Container/Container";

function NotFoundPage() {
	return (
		<div className="flex items-center justify-center bg-bg">
			<Container>
				<div className="mx-auto max-w-xl text-center">
					<p className="font-dancing text-9xl font-bold text-primary/20 select-none">
						404
					</p>

					<h1 className="mt-2 text-4xl font-bold text-t-primary">Oops! Page not found</h1>

					<p className="mx-auto mt-4 max-w-md text-lg text-t-muted">
						The page you're looking for doesn't exist, may have been moved, or the URL
						might be incorrect.
					</p>
				</div>
			</Container>
		</div>
	);
}

export default NotFoundPage;
