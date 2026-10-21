import { useSelector } from "react-redux";
import { useNavigate } from "react-router";

import Container from "@/components/Container";
import FormPageHeader from "@/components/FormPageHeader";
import OAuthConnectionsCard from "@/components/Pages/Profile/OAuthConnectionsCard";
import ProfileDetailsCard from "@/components/Pages/Profile/ProfileDetailsCard";

function ProfilePage() {
	const navigate = useNavigate();
	const user = useSelector((state) => state.auth.user);

	return (
		<Container className="space-y-8">
			<FormPageHeader
				backLabel="Dashboard"
				onBack={() => {
					navigate("/dashboard");
				}}
				title="Profile Settings"
				description="Manage your personal information, profile photo, and account settings."
			/>

			<ProfileDetailsCard user={user} />
			{/* <DeleteAccountCard /> */}
			<OAuthConnectionsCard />
		</Container>
	);
}

export default ProfilePage;
