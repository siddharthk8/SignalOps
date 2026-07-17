export default function Footer() {
	return (
		<footer className="bg-surface text-t-secondary border-border border-t shadow-sm">
			<div className="mx-auto flex max-w-7xl flex-col items-center justify-between gap-2 px-4 py-4 text-sm sm:flex-row">
				<span>
					© 2026{" "}
					<span className="text-t-primary font-dancing text-lg font-medium">
						SignalOps
					</span>
					. All rights reserved.
				</span>

				<span className="text-t-muted">
					✨ Built with care by{" "}
					<span className="text-t-primary font-dancing text-lg">Siddharth</span>
				</span>
			</div>
		</footer>
	);
}
