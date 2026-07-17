const Container = ({ className = "", children }) => {
	return (
		<div className={`text-t-primary bg-bg px-8 py-12 md:px-16 lg:px-24 ${className}`}>
			{children}
		</div>
	);
};

export default Container;
