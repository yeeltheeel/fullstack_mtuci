import type { Location } from '../data/Types';
import LocationCard from "../components/LocationCard";
import NoContentCard from "../components/NoContentCard";

import { test_locations } from "../data/MockData";

type Prop = {
	locations: Array<Location>;
}

export default function LocationsPage({ locations }: Prop) {
	return (
		<div className="list_display">
			<h1>Our Locations</h1>
			{test_locations.length > 0 ? (
				test_locations.map((location) => (
					<LocationCard location={location} key={location.id} />
				))
			) : (
				<NoContentCard />
			)}
		</div>
	)
}