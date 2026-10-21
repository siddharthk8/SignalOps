const sections = [
	{
		id: "introduction",
		title: "Introduction",
		content: (
			<>
				<p>
					SignalOps is an application log intelligence platform that helps developers and
					engineering teams analyze logs, identify operational signals, correlate
					incidents, and generate AI-assisted insights.
				</p>
				<p>
					This Privacy Policy explains how information is collected, processed, stored,
					and shared when you use SignalOps.
				</p>
			</>
		),
	},
	{
		id: "information",
		title: "Information We Process",
		content: (
			<>
				<p>Depending on how you use SignalOps, information may include:</p>
				<ul className="marker:text-primary my-4 list-disc space-y-2 pl-5">
					<li>
						<strong className="text-t-primary font-semibold">
							Account information:
						</strong>{" "}
						Name, email address, account identifier, profile picture, and authentication
						records.
					</li>
					<li>
						<strong className="text-t-primary font-semibold">Application logs:</strong>{" "}
						Timestamps, error messages, stack traces, IP addresses, request identifiers,
						and other technical data contained in submitted logs.
					</li>
					<li>
						<strong className="text-t-primary font-semibold">
							Derived information:
						</strong>{" "}
						Normalized events, detection signals, incident records, timelines, dashboard
						data, and AI-generated analysis.
					</li>
					<li>
						<strong className="text-t-primary font-semibold">
							Technical information:
						</strong>{" "}
						Browser and device details, session identifiers, and security-related
						records.
					</li>
				</ul>
				<p>
					Application logs may contain personal, confidential, or security-sensitive
					information. Submit only information you are authorized to process and avoid
					including passwords, access tokens, private keys, or other unnecessary secrets.
				</p>
			</>
		),
	},
	{
		id: "usage",
		title: "How Information Is Used",
		content: (
			<>
				<p>Information is processed to:</p>
				<ul className="marker:text-primary my-4 list-disc space-y-2 pl-5">
					<li>Create and authenticate accounts.</li>
					<li>Receive, parse, and analyze application logs.</li>
					<li>Generate events, signals, incidents, and AI-assisted insights.</li>
					<li>Display dashboards and analysis results.</li>
					<li>
						Maintain platform functionality, troubleshoot issues, and help protect
						against misuse.
					</li>
					<li>Meet applicable legal requirements.</li>
				</ul>
			</>
		),
	},
	{
		id: "google-sign-in",
		title: "Google Sign-In",
		content: (
			<>
				<p>
					SignalOps supports Google Sign-In. Depending on the permissions granted, we may
					receive your name, email address, profile picture, and Google account
					identifier.
				</p>
				<p>
					The authentication flow uses the <code>openid</code>, <code>email</code>, and{" "}
					<code>profile</code> scopes. It does not request access to Gmail messages,
					Google Drive files, or Google Calendar.
				</p>
				<p>
					Google account information is used for authentication, account management, and
					associated platform functionality. Google user data is not sold, used for
					advertising, or used to train generalized AI models.
				</p>
				<p>
					See the{" "}
					<a
						href="https://policies.google.com/privacy"
						target="_blank"
						rel="noopener noreferrer"
						className="text-primary-700 decoration-primary-400/60 hover:text-primary-800 dark:text-primary-700 underline underline-offset-4"
					>
						Google Privacy Policy
					</a>{" "}
					for information about Google's privacy practices.
				</p>
			</>
		),
	},
	{
		id: "logs-ai",
		title: "Log Storage and AI Processing",
		content: (
			<>
				<p>
					SignalOps processes application logs through a pipeline that may include
					validation, parsing, event normalization, detection rules, incident correlation,
					and AI-assisted analysis.
				</p>
				<p>
					Depending on the features used, raw logs and derived records may be stored to
					support dashboards, incident history, debugging, and analysis.
				</p>
				<p>
					SignalOps uses Amazon Bedrock for AI-assisted operational analysis. Relevant log
					content, derived events, incident context, and technical metadata may be sent to
					Amazon Bedrock when AI analysis is requested.
				</p>
				<p>
					AI-generated summaries, potential causes, and recommendations may be incomplete
					or inaccurate. Review results independently before relying on them for
					operational or security decisions.
				</p>
				<p>
					See the{" "}
					<a
						href="https://docs.aws.amazon.com/bedrock/latest/userguide/data-protection.html"
						target="_blank"
						rel="noopener noreferrer"
						className="text-primary-700 decoration-primary-400/60 hover:text-primary-800 dark:text-primary-700 underline underline-offset-4"
					>
						AWS Bedrock data protection documentation
					</a>{" "}
					for information about its data-handling practices.
				</p>
			</>
		),
	},
	{
		id: "retention",
		title: "Data Retention and Deletion",
		content: (
			<>
				<p>
					Information may be retained for as long as needed to provide platform
					functionality, maintain relevant records, support security, or meet applicable
					legal requirements.
				</p>
				<p>
					Deleting a record through an available platform control may not immediately
					remove associated events, incidents, cached copies, backups, or security
					records. Retention and deletion behavior depends on the features implemented and
					the storage systems involved.
				</p>
				<p>
					For account or data-related requests, use the contact information provided
					below.
				</p>
			</>
		),
	},
	{
		id: "sharing",
		title: "Sharing and Third-Party Services",
		content: (
			<>
				<p>SignalOps does not sell personal information or application logs.</p>
				<p>
					Information may be processed by third-party services used to operate the
					platform, including Google Identity Services for authentication and Amazon
					Bedrock for AI analysis. Relevant information may also be disclosed where
					required by law or reasonably necessary to address security issues or misuse.
				</p>
				<p>
					Third-party services handle information under their applicable terms and privacy
					practices.
				</p>
			</>
		),
	},
	{
		id: "security",
		title: "Security, Cookies, and Privacy Choices",
		content: (
			<>
				<p>
					SignalOps uses measures intended to help protect stored information and account
					access. No online service or data transmission method can be guaranteed to be
					completely secure.
				</p>
				<p>
					Cookies and session identifiers may be used for authentication, session
					management, preferences, and essential platform functionality. Any non-essential
					tracking technologies, if introduced, will be handled in accordance with
					applicable requirements.
				</p>
				<p>
					Where supported by the platform and applicable law, users may update account
					information, delete available records, or request account deletion. Some
					information may remain temporarily in backups or be retained where legally
					permitted or required.
				</p>
				<p>
					SignalOps is not intended for children whose use of the service is prohibited by
					applicable law.
				</p>
			</>
		),
	},
	{
		id: "updates-contact",
		title: "Policy Updates and Contact",
		content: (
			<>
				<p>
					This Privacy Policy may be updated as SignalOps evolves or its data practices
					change. The latest version and revision date will be published on this page. By
					accessing or using SignalOps, you acknowledge that you have read and understood
					this Privacy Policy. If you have questions about how your information is
					handled, please contact us using the details provided below.
				</p>
				<div className="border-border mt-5 border-t pt-5">
					<p className="text-t-primary font-medium">SignalOps</p>
					<p className="text-t-muted mt-3 text-sm">Website</p>
					<a
						href="https://signalops.siddharthkr.com"
						className="text-primary-700 hover:text-primary-800 dark:text-primary-700 break-all underline underline-offset-4"
					>
						signalops.siddharthkr.com
					</a>
					<p className="text-t-muted mt-4 text-sm">Privacy contact</p>
					<a
						href="mailto:contact@siddharthkr.com"
						className="text-primary-700 hover:text-primary-800 dark:text-primary-700 break-all underline underline-offset-4"
					>
						contact@siddharthkr.com
					</a>
				</div>
			</>
		),
	},
];

export default function PrivacyPolicy() {
	return (
		<main className="bg-bg text-t-primary min-h-screen">
			<header className="border-border bg-surface border-b">
				<div className="mx-auto max-w-6xl px-5 py-12 sm:px-8 sm:py-16">
					<p className="text-primary-700 dark:text-primary-700 text-sm font-semibold tracking-wide">
						SIGNALOPS / LEGAL
					</p>
					<h1 className="mt-4 text-3xl font-semibold tracking-tight sm:text-4xl">
						Privacy Policy
					</h1>
					<p className="text-t-secondary mt-4 max-w-2xl text-sm leading-7 sm:text-base">
						How SignalOps collects, uses, and handles account information and
						application logs.
					</p>
					<p className="text-t-muted mt-6 text-xs font-medium">
						LAST UPDATED · OCTOBER 21, 2026
					</p>
				</div>
			</header>

			<div className="mx-auto grid max-w-6xl grid-cols-1 gap-10 px-5 py-10 sm:px-8 sm:py-14 lg:grid-cols-[200px_minmax(0,1fr)] lg:gap-16">
				<aside className="h-fit lg:sticky lg:top-8">
					<p className="text-t-muted mb-4 text-xs font-semibold tracking-widest uppercase">
						Contents
					</p>
					<nav className="grid grid-cols-1 gap-1 sm:grid-cols-2 lg:grid-cols-1">
						{sections.map((section, index) => (
							<a
								key={section.id}
								href={`#${section.id}`}
								className="text-t-secondary hover:bg-elevated hover:text-primary-700 dark:hover:text-primary-700 flex items-start gap-3 rounded-lg px-3 py-2 text-sm transition"
							>
								<span className="text-t-muted w-5 shrink-0 pt-0.5 text-xs tabular-nums">
									{String(index + 1).padStart(2, "0")}
								</span>
								<span>{section.title}</span>
							</a>
						))}
					</nav>
				</aside>

				<article className="min-w-0">
					<div className="border-border mb-8 border-b pb-6">
						<p className="text-t-secondary text-sm leading-7">
							This policy covers the information processed through SignalOps and the
							third-party services used to provide its features.
						</p>
					</div>

					<div className="divide-border divide-y">
						{sections.map((section, index) => (
							<section
								key={section.id}
								id={section.id}
								className="scroll-mt-8 py-7 first:pt-0 last:pb-0 sm:py-8"
							>
								<div className="mb-4 flex items-baseline gap-4">
									<span className="text-primary-700 dark:text-primary-700 text-xs font-medium tabular-nums">
										{String(index + 1).padStart(2, "0")}
									</span>
									<h2 className="text-t-primary text-lg font-semibold tracking-tight sm:text-xl">
										{section.title}
									</h2>
								</div>
								<div className="text-t-secondary space-y-4 pl-0 text-sm leading-7 sm:pl-9 sm:text-[15px]">
									{section.content}
								</div>
							</section>
						))}
					</div>

					<div className="border-border text-t-muted mt-10 border-t pt-6 text-xs leading-6">
						SignalOps · Privacy Policy
					</div>
				</article>
			</div>
		</main>
	);
}
