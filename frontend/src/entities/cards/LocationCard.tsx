import type { Location } from '../../data/Types';
import Modal from '../ui/Modal';
import LocationIcon from '../../shared/icons/university.png';
import DetailsIcon from '../../shared/icons/menu.png';
import LocationDetails from "../info/LocationDetails";

type Props = {
	location: Location;
}

export default function LocationCard({ location }: Props) {
	const modal = Modal();
	return (
		<div className="card">
			<div className="card_img">
				<img src={LocationIcon} />
			</div>
			<div>
				<h2>{location.street}, {location.house}</h2>
				<h4>{location.country}, {location.city}</h4>
			</div>
			<div className="details_button">
				<button onClick={() =>
					modal.open({
						body: <LocationDetails location={location} onClose={() => modal.close()}/>,
					})}>
					<img src={DetailsIcon} alt="Show details" />
				</button>
			</div>
		</div>
	)
}