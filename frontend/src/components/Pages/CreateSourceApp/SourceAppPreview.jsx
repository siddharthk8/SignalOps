import { CheckCircle2, CreditCard, Shield, ShoppingCart } from "lucide-react";

const APP_TYPES = {
	"auth-app": {
		icon: Shield,
		title: "Authentication",
		description:
			"Monitor login attempts, MFA failures, password resets, and suspicious account activity.",
		color: "text-primary",
		bg: "bg-primary/10",
		features: ["Login attempts", "MFA failures", "Account lockouts"],
	},
	"payment-app": {
		icon: CreditCard,
		title: "Payments",
		description:
			"Track payment processing, failed transactions, fraud detection, and billing events.",
		color: "text-warning",
		bg: "bg-warning/10",
		features: ["Failed transactions", "Fraud detection", "Refund events"],
	},
	"order-app": {
		icon: ShoppingCart,
		title: "Order Management",
		description:
			"Monitor order creation, fulfillment, cancellations, inventory, and delivery workflows.",
		color: "text-success",
		bg: "bg-success/10",
		features: ["Order cancellations", "Inventory updates", "Delivery events"],
	},
};

function SourceAppPreview({ appType }) {
	const app = APP_TYPES[appType];

	const Icon = app.icon;

	return (
		<aside className="border-border bg-surface rounded-lg border">
			<div className="border-border border-b px-6 py-5">
				<h2 className="text-t-primary text-lg font-semibold">Application Preview</h2>

				<p className="text-t-muted mt-1 text-sm">Based on the selected application type.</p>
			</div>

			<div className="space-y-6 p-6">
				<div className={`flex size-14 items-center justify-center rounded-lg ${app.bg}`}>
					<Icon size={28} className={app.color} />
				</div>

				<div>
					<h3 className="text-t-primary text-xl font-semibold">{app.title}</h3>
					<p className="text-t-muted mt-2 text-sm leading-7">{app.description}</p>
				</div>

				<div className="border-border border-t pt-6">
					<p className="text-t-primary mb-4 text-sm font-medium">
						Common events you'll monitor
					</p>

					<div className="space-y-3">
						{app.features.map((feature) => (
							<div key={feature} className="flex items-center gap-3">
								<CheckCircle2 size={16} className="text-success shrink-0" />

								<span className="text-t-muted text-sm">{feature}</span>
							</div>
						))}
					</div>
				</div>
			</div>
		</aside>
	);
}

export default SourceAppPreview;
