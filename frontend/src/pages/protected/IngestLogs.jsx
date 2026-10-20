import { ArrowRight, Code2, FlaskConical, KeyRound, Terminal } from "lucide-react";
import { useNavigate, useParams } from "react-router";

import Button from "@/components/Button";
import Container from "@/components/Container";

export default function LogIngestionOptionsPage() {
	const navigate = useNavigate();
	const { sourceAppId } = useParams();

	const options = [
		{
			title: "Playground",
			subtitle: "Test log ingestion interactively",
			description:
				"Build a JSON payload, submit logs directly from your dashboard, and validate your ingestion workflow without writing client-side integration code.",
			icon: FlaskConical,
			iconStyle: "bg-accent/10 text-accent",
			tag: "Interactive testing",
			features: [
				"Editable JSON request payload",
				"Immediate API submission",
				"Validate log formats and fields",
			],
			buttonLabel: "Open Playground",
			onClick: () => navigate(`playground`),
		},
		{
			title: "API Integration",
			subtitle: "Send logs from your application",
			description:
				"Generate and manage an access token, integrate the ingestion endpoint into your application, and use ready-to-copy API examples.",
			icon: KeyRound,
			iconStyle: "bg-primary/10 text-primary",
			tag: "Production",
			features: [
				"Generate, rotate, or revoke access tokens",
				"Axios and cURL integration examples",
				"Authentication and request documentation",
			],
			buttonLabel: "Configure API Access",
			onClick: () => navigate(`api-access`),
		},
	];

	return (
		<Container>
			<div className="mx-auto max-w-5xl space-y-8 py-4">
				<div className="space-y-3">
					<div className="bg-primary/10 text-primary flex h-12 w-12 items-center justify-center rounded-xl">
						<Terminal size={24} />
					</div>

					<div>
						<p className="text-t-muted mb-2 text-sm font-medium">Developer tools</p>

						<h1 className="font-['Space_Grotesk'] text-3xl font-bold tracking-tight">
							Log Ingestion
						</h1>

						<p className="text-t-muted mt-2 max-w-2xl text-sm leading-6">
							Choose how you want to send logs to this application. Test requests in
							the playground or integrate the API into your own application.
						</p>
					</div>
				</div>

				<div className="grid gap-5 md:grid-cols-2">
					{options.map((option) => {
						const Icon = option.icon;

						return (
							<section
								key={option.title}
								className="border-border bg-surface flex flex-col rounded-xl border p-6 shadow-sm transition hover:shadow-md"
							>
								<div className="flex items-start justify-between gap-3">
									<div
										className={`flex h-12 w-12 items-center justify-center rounded-xl ${option.iconStyle}`}
									>
										<Icon size={23} />
									</div>

									<span className="bg-muted text-t-muted rounded-full px-3 py-1 text-xs font-medium">
										{option.tag}
									</span>
								</div>

								<div className="mt-5">
									<h2 className="font-['Space_Grotesk'] text-xl font-semibold">
										{option.title}
									</h2>

									<p className="text-t-secondary mt-1 text-sm font-medium">
										{option.subtitle}
									</p>

									<p className="text-t-muted mt-3 text-sm leading-6">
										{option.description}
									</p>
								</div>

								<ul className="mt-6 flex-1 space-y-3">
									{option.features.map((feature) => (
										<li
											key={feature}
											className="text-t-secondary flex items-start gap-2 text-sm"
										>
											<Code2
												size={16}
												className="text-primary mt-0.5 shrink-0"
											/>
											<span>{feature}</span>
										</li>
									))}
								</ul>

								<div className="border-border mt-7 border-t pt-5">
									<Button
										type="button"
										className="w-full"
										rightIcon={<ArrowRight size={16} />}
										onClick={option.onClick}
									>
										{option.buttonLabel}
									</Button>
								</div>
							</section>
						);
					})}
				</div>

				<div className="border-border bg-muted/20 flex items-start gap-3 rounded-lg border p-4">
					<Code2 className="text-t-muted mt-0.5 shrink-0" size={19} />

					<div>
						<p className="text-sm font-medium">Not sure where to start?</p>
						<p className="text-t-muted mt-1 text-sm leading-6">
							Use the Playground to try your first request. When you're ready to
							integrate log ingestion into your application, configure API access.
						</p>
					</div>
				</div>
			</div>
		</Container>
	);
}
