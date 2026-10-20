import { Menu, Monitor, Moon, Sun, X } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { NavLink, useLocation, useNavigate } from "react-router";

import useTheme from "@/shared/hooks/useTheme";

import HoverButton from "../Button/HoverButton";
import Logo from "../Logo";
import AuthNavbar from "./AuthNavbar";
import UnauthNavbar from "./UnAuthNavbar";

export default function Navbar({ auth }) {
	const [isUserMenuOpen, setIsUserMenuOpen] = useState(false);
	const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
	const [isThemeMenuOpen, setIsThemeMenuOpen] = useState(false);

	const userMenuRef = useRef(null);
	const mobileMenuRef = useRef(null);
	const mobileButtonRef = useRef(null);
	const themeMenuRef = useRef(null);

	const navigate = useNavigate();
	const location = useLocation();

	const { theme, systemTheme, setTheme } = useTheme();
	const currentTheme = theme === "system" ? systemTheme : theme;
	const ThemeIcon = currentTheme === "dark" ? Moon : Sun;

	const themeItems = [
		{ name: "Light", value: "light", icon: Sun },
		{ name: "Dark", value: "dark", icon: Moon },
		{ name: "System", value: "system", icon: Monitor },
	];

	const navItems =
		location.pathname === "/"
			? [
					{
						name: "Philosophy",
						link: "#philosophy",
						isActive: location.hash === "#philosophy",
					},
					{
						name: "Features",
						link: "#features",
						isActive: location.hash === "#features",
					},
					{
						name: "Architecture",
						link: "#architecture",
						isActive: location.hash === "#architecture",
					},
					{
						name: "Workflow",
						link: "#workflow",
						isActive: location.hash === "#workflow",
					},
					{
						name: "Technology",
						link: "#technology",
						isActive: location.hash === "#technology",
					},
				]
			: auth.user
				? [
						{
							name: "Dashboard",
							link: "/dashboard",
							isActive: location.pathname === "/dashboard",
						},
						{
							name: "Source Apps",
							link: "/source-apps",
							isActive: location.pathname === "/source-apps",
						},
						{
							name: "Create Source App",
							link: "/create-source-app",
							isActive: location.pathname === "/create-source-app",
						},
					]
				: null;

	const toggleThemeMenu = () => {
		setIsThemeMenuOpen((value) => !value);
		setIsUserMenuOpen(false);
		setIsMobileMenuOpen(false);
	};

	useEffect(() => {
		const handleClickOutside = (e) => {
			if (themeMenuRef.current && !themeMenuRef.current.contains(e.target)) {
				setIsThemeMenuOpen(false);
			}
			if (userMenuRef.current && !userMenuRef.current.contains(e.target)) {
				setIsUserMenuOpen(false);
			}
			if (
				mobileMenuRef.current &&
				!mobileMenuRef.current.contains(e.target) &&
				mobileButtonRef.current &&
				!mobileButtonRef.current.contains(e.target)
			) {
				setIsMobileMenuOpen(false);
			}
		};

		const handleKeyDown = (e) => {
			if (e.key === "Escape") {
				setIsThemeMenuOpen(false);
				setIsUserMenuOpen(false);
				setIsMobileMenuOpen(false);
			}
		};

		document.addEventListener("mousedown", handleClickOutside);
		document.addEventListener("keydown", handleKeyDown);

		return () => {
			document.removeEventListener("mousedown", handleClickOutside);
			document.removeEventListener("keydown", handleKeyDown);
		};
	}, []);

	return (
		<nav className="bg-surface border-border text-t-primary fixed top-0 right-0 left-0 border-b">
			<div className="mx-auto max-w-7xl px-3 sm:px-4 md:px-8">
				{/*
					⚠️ If you change h-14 / sm:h-16 below,
					remember to update scroll-padding-top in html{} in index.css accordingly.
					+ also Edit the Layout.jsx
				*/}
				<div className="flex h-14 items-center justify-between sm:h-16">
					{/* Left – shared */}
					<div className="flex flex-1 items-center gap-4">
						<button
							onClick={() => {
								if (location.pathname == "/") {
									// On MainScreen the user will press on this to go to top.
									window?.scrollTo({ top: 0 });

									// Remove the hash from URL
									window?.history?.replaceState(
										null,
										"",
										window.location.pathname + window.location.search,
									);
								} else if (auth.user) {
									// Authenticated User
									navigate("/dashboard");
								} else {
									// Unauthenticated User (Ex: On Login Screen)
									navigate("/");
								}
							}}
							className="flex cursor-pointer items-center gap-2 text-base font-medium sm:text-lg"
						>
							<Logo className="h-5 w-8 overflow-hidden sm:h-6 sm:w-10" />
							<span className="font-dancing text-2xl font-medium">
								<span className="text-primary-500 font-bold">S</span>ignal
								<span className="text-accent-500 ml-1 font-bold">O</span>ps
							</span>
						</button>

						{/* Desktop nav */}
						{navItems && (
							<nav className="hidden flex-1 items-center justify-center md:flex">
								<div className="bg-background flex items-center gap-1 rounded-lg p-1">
									{navItems.map((item) => (
										<NavLink
											key={item.name}
											replace
											to={item.link}
											className={`text-md relative rounded-md px-4 py-2 font-medium transition-all duration-200 ${
												item.isActive
													? "bg-surface text-primary shadow-sm"
													: "text-t-muted hover:bg-surface hover:text-t-primary"
											}`}
										>
											{item.name}

											{item.isActive && (
												<span className="bg-primary absolute inset-x-3 bottom-0 h-0.5 rounded-full" />
											)}
										</NavLink>
									))}
								</div>
							</nav>
						)}
					</div>

					{/* Right – variant */}
					<div className="flex items-center gap-2 sm:gap-4">
						{/* Theme switcher */}
						<div ref={themeMenuRef} className="relative">
							<HoverButton onClick={toggleThemeMenu}>
								<ThemeIcon className="text-t-primary h-6 w-6" />
							</HoverButton>

							{isThemeMenuOpen && (
								<div className="bg-surface border-border absolute right-0 z-50 mt-2 w-40 rounded-lg border shadow-lg">
									<div className="px-2 py-1">
										{themeItems.map((item) => {
											const Icon = item.icon;
											return (
												<button
													key={item.value}
													onClick={() => {
														setTheme(item.value);
														setIsThemeMenuOpen(false);
													}}
													className={`my-1 flex w-full items-center gap-2 rounded-md px-3 py-2 text-sm transition ${
														theme === item.value
															? "bg-surface-elevated"
															: "hover:bg-surface-elevated"
													}`}
												>
													<Icon className="h-5 w-5" />
													{item.name}
												</button>
											);
										})}
									</div>
								</div>
							)}
						</div>

						{auth.user ? (
							<AuthNavbar
								auth={auth}
								isUserMenuOpen={isUserMenuOpen}
								setIsUserMenuOpen={setIsUserMenuOpen}
								userMenuRef={userMenuRef}
							/>
						) : (
							<UnauthNavbar />
						)}

						{navItems && (
							<button
								ref={mobileButtonRef}
								onClick={() => setIsMobileMenuOpen((p) => !p)}
								className="hover:bg-surface-elevated rounded-lg p-2 md:hidden"
							>
								{isMobileMenuOpen ? (
									<X className="h-6 w-6" />
								) : (
									<Menu className="h-6 w-6" />
								)}
							</button>
						)}

						{navItems && isMobileMenuOpen && (
							<div
								ref={mobileMenuRef}
								className="border-border bg-surface absolute top-full left-0 w-full border-t md:hidden"
							>
								{navItems.map((item) => (
									<NavLink
										key={item.name}
										to={item.link}
										className="my-1 block px-4 py-2"
										onClick={(e) => {
											setIsMobileMenuOpen(false);
										}}
									>
										{item.name}
									</NavLink>
								))}
							</div>
						)}
					</div>
				</div>
			</div>
		</nav>
	);
}
