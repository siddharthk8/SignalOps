import { useMutation } from "@tanstack/react-query";
import { ChevronDown } from "lucide-react";
import { useDispatch } from "react-redux";
import { useNavigate } from "react-router";

import { revokeAllRefreshTokens, revokeRefreshToken } from "@/api";
import authenticatedClient from "@/core/api/customClient";
import { clearUser } from "@/store/features/authSlice";

import Avatar from "../Avatar";
import HoverButton from "../Button/HoverButton";

export default function AuthNavbar({ auth, isUserMenuOpen, setIsUserMenuOpen, userMenuRef }) {
	const navigate = useNavigate();
	const dispatch = useDispatch();

	const userLogoutMutation = useMutation({
		mutationFn: ({ refresh_token }) =>
			revokeRefreshToken({
				client: authenticatedClient,
				body: {
					refresh_token: refresh_token,
				},
			}),
		onSuccess: () => {
			dispatch(clearUser());
		},
	});
	const revokeAllLogoutMutation = useMutation({
		mutationFn: () =>
			revokeAllRefreshTokens({
				client: authenticatedClient,
			}),
		onSuccess: () => {
			dispatch(clearUser());
		},
	});

	const userMenuItems = [
		{ name: "Your Profile", link: "/profile" },
		{ name: "Change Password", link: "/change-password" },
		{ name: "Sign out" },
		{ name: "Sign out from all devices" },
	];

	return (
		<div ref={userMenuRef} className="relative">
			<HoverButton
				onClick={() => setIsUserMenuOpen((p) => !p)}
				className="flex items-center gap-2"
			>
				<Avatar
					firstName={auth.user.firstName}
					lastName={auth.user.lastName}
					profileImage={auth.user.profileImage}
					size="sm"
				/>
				<ChevronDown
					className={`w-4 h-4 sm:w-5 sm:h-5 transition-transform ${
						isUserMenuOpen ? "rotate-180" : ""
					}`}
				/>
			</HoverButton>

			{isUserMenuOpen && (
				<div className="absolute right-0 mt-2 w-52 sm:w-56 rounded-lg bg-surface border border-border shadow-lg z-50">
					<div className="py-1 px-2">
						{userMenuItems.map((item) => (
							<button
								key={item.name}
								onClick={() => {
									setIsUserMenuOpen(false);
									if (
										item.name === "Sign out" ||
										item.name === "Sign out from all devices"
									) {
										if (item.name === "Sign out from all devices") {
											// request server to sign out from all devices
											revokeAllLogoutMutation.mutate();
										} else {
											// request server to sign out from current device
											userLogoutMutation.mutate({
												refresh_token: auth.user.refreshToken,
											});
										}
									} else {
										navigate(item.link);
									}
								}}
								className="w-full px-3 py-2 my-1 text-sm text-left rounded-md hover:bg-surface-elevated"
							>
								{item.name}
							</button>
						))}
					</div>
				</div>
			)}
		</div>
	);
}
