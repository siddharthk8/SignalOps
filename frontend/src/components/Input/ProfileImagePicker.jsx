import { Camera, Loader2, User, X } from "lucide-react";
import { useEffect, useMemo } from "react";

export default function ProfileImagePicker({ value, loading, onChange }) {
	const previewUrl = useMemo(() => {
		if (!value) return null;

		if (typeof value === "string") {
			return value;
		}

		return URL.createObjectURL(value);
	}, [value]);

	useEffect(() => {
		return () => {
			if (value instanceof File && previewUrl) {
				URL.revokeObjectURL(previewUrl);
			}
		};
	}, [previewUrl, value]);

	const handleChange = (e) => {
		const file = e.target.files?.[0];
		if (!file) return;

		onChange(file);
	};

	const handleRemove = () => {
		onChange(null);
	};

	return (
		<div className="flex items-center gap-5">
			<div className="group relative">
				<label
					className={`border-border bg-muted relative block h-32 w-32 overflow-hidden rounded-full border shadow-sm transition ${
						loading
							? "cursor-not-allowed"
							: "hover:ring-primary/30 cursor-pointer hover:ring-2"
					}`}
				>
					{previewUrl ? (
						<img
							src={previewUrl}
							alt="Profile"
							className="h-full w-full object-cover"
						/>
					) : (
						<div className="flex h-full w-full items-center justify-center">
							<User className="text-muted-foreground/60 h-12 w-12" />
						</div>
					)}

					<input
						type="file"
						accept="image/*"
						className="hidden"
						onChange={handleChange}
						disabled={loading}
					/>

					<div className="absolute inset-0 flex items-center justify-center bg-black/55 opacity-0 transition-opacity group-hover:opacity-100">
						<div className="flex flex-col items-center text-white">
							<Camera size={18} />
							<span className="mt-1 text-xs font-medium">
								{previewUrl ? "Change photo" : "Upload"}
							</span>
						</div>
					</div>

					{loading && (
						<div className="absolute inset-0 flex items-center justify-center bg-black/60">
							<Loader2 className="h-6 w-6 animate-spin text-white" />
						</div>
					)}
				</label>

				{previewUrl && !loading && (
					<button
						type="button"
						onClick={handleRemove}
						className="bg-background hover:bg-destructive absolute -top-1 -right-1 flex h-7 w-7 items-center justify-center rounded-full border shadow transition hover:text-white"
					>
						<X size={14} />
					</button>
				)}
			</div>

			<div className="space-y-1">
				<h3 className="font-medium">Profile photo</h3>

				<p className="text-muted-foreground text-sm">
					Upload a square image for the best results.
				</p>

				<p className="text-muted-foreground text-xs">JPG, PNG or WebP • Max 5 MB</p>
			</div>
		</div>
	);
}
