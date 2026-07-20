export default function isEmptyData(data) {
	if (data == null) return true; // null or undefined

	if (Array.isArray(data)) {
		return data.length === 0;
	}

	if (typeof data === "object") {
		return Object.keys(data).length === 0;
	}

	return false;
}
