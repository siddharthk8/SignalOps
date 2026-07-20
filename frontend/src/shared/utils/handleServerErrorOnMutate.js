import axios from "axios";

import { SERVER_ERROR_MSG } from "@/shared/constants/messages";

export function handleServerErrorOnMutate(error, setError) {
	if (!axios.isAxiosError(error)) {
		setError("root", {
			type: "server",
			message: SERVER_ERROR_MSG,
		});
		return;
	}

	const data = error.response?.data;

	setError(data?.field ?? "root", {
		type: "server",
		message: data?.message ?? SERVER_ERROR_MSG,
	});
}
