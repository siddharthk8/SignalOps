import { useEffect, useState } from "react";

export default function useResendCoolDown(duration = 120) {
	const [secondsLeft, setSecondsLeft] = useState(0);

	const startCooldown = () => {
		setSecondsLeft(duration);
	};

	const resetCooldown = () => {
		setSecondsLeft(0);
	};

	useEffect(() => {
		if (secondsLeft <= 0) return;

		const interval = setInterval(() => {
			setSecondsLeft((prev) => prev - 1);
		}, 1000);

		return () => clearInterval(interval);
	}, [secondsLeft]);

	const isCooldownActive = secondsLeft > 0;

	const formattedTime = `${String(Math.floor(secondsLeft / 60)).padStart(
		2,
		"0",
	)}:${String(secondsLeft % 60).padStart(2, "0")}`;

	return {
		secondsLeft,
		formattedTime,
		isCooldownActive,
		startCooldown,
		resetCooldown,
	};
}
