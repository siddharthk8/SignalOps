export default function getVisiblePages(currentPage, totalPages) {
	if (totalPages <= 0) return [];

	const start = Math.max(0, Math.min(currentPage - 1, totalPages - 3));
	return Array.from({ length: Math.min(3, totalPages) }, (_, i) => start + i);
}
