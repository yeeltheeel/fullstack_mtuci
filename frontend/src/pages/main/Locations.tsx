import { useLoaderData } from "react-router";
import type { Location } from '../../data/Types';
import LocationCard from "../../entities/cards/LocationCard";
import NoContentCard from "../../entities/cards/NoContentCard";

export default function LocationsPage() {
	const { locations } = useLoaderData() as { locations: Location[] };
	return (
		<div className="list_display">
			<h1>Our Locations</h1>
			{locations.length > 0 ? (
				locations.map((location) => (
					<LocationCard location={location} key={location.id} />
				))
			) : (
				<NoContentCard />
			)}
		</div>
	)
}