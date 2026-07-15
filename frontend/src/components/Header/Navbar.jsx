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
							link: "/dashboard/source-apps",
							isActive: location.pathname === "/dashboard/source-apps",
						},
						{
							name: "Create Source App",
							link: "/dashboard/create-source-app",
							isActive: location.pathname === "/dashboard/create-source-app",
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
		<nav className="bg-surface border-b border-border fixed top-0 left-0 right-0 text-t-primary">
			<div className="max-w-7xl mx-auto px-3 sm:px-4 md:px-8">
				{/*
					⚠️ If you change h-14 / sm:h-16 below,
					remember to update scroll-padding-top in html{} in index.css accordingly.
					+ also Edit the Layout.jsx
				*/}
				<div className="flex h-14 sm:h-16 items-center justify-between">
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
							className="flex items-center gap-2 text-base sm:text-lg font-medium cursor-pointer"
						>
							<Logo className="w-5 h-5 sm:w-6 sm:h-6" />
							<span className="font-medium text-2xl font-dancing">
								<span className="font-bold text-primary-500">S</span>ignal
								<span className="font-bold text-accent-500 ml-1">O</span>ps
							</span>
						</button>

						{/* Desktop nav */}
						{navItems && (
							<div className="hidden md:flex flex-1 justify-center items-center gap-6 lg:gap-8">
								{navItems.map((item) => (
									<NavLink
										replace
										to={item.link}
										key={item.name}
										className={`text-sm lg:text-base font-medium transition-colors ${
											item.isActive
												? "text-primary"
												: "text-t-muted hover:text-primary"
										}`}
									>
										{item.name}
									</NavLink>
								))}
							</div>
						)}
					</div>

					{/* Right – variant */}
					<div className="flex items-center gap-2 sm:gap-4">
						{/* Theme switcher */}
						<div ref={themeMenuRef} className="relative">
							<HoverButton onClick={toggleThemeMenu}>
								<ThemeIcon className="w-6 h-6 text-t-primary" />
							</HoverButton>

							{isThemeMenuOpen && (
								<div className="absolute right-0 mt-2 w-40 rounded-lg bg-surface border border-border shadow-lg z-50">
									<div className="py-1 px-2">
										{themeItems.map((item) => {
											const Icon = item.icon;
											return (
												<button
													key={item.value}
													onClick={() => {
														setTheme(item.value);
														setIsThemeMenuOpen(false);
													}}
													className={`w-full flex my-1 items-center gap-2 px-3 py-2 rounded-md text-sm transition ${
														theme === item.value
															? "bg-surface-elevated"
															: "hover:bg-surface-elevated"
													}`}
												>
													<Icon className="w-5 h-5" />
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
								className="md:hidden p-2 rounded-lg hover:bg-surface-elevated"
							>
								{isMobileMenuOpen ? (
									<X className="w-6 h-6" />
								) : (
									<Menu className="w-6 h-6" />
								)}
							</button>
						)}

						{navItems && isMobileMenuOpen && (
							<div
								ref={mobileMenuRef}
								className="absolute top-full left-0 w-full border-t border-border bg-surface md:hidden"
							>
								{navItems.map((item) => (
									<NavLink
										key={item.name}
										to={item.link}
										className="block px-4 py-2 my-1"
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
