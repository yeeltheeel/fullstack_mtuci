import type { Location } from '../../data/Types';
import { useNavigate } from 'react-router';
import { print_short, print_full } from '../../data/Local';

type Props = {
	location: Location;
	onClose: () => void;
}

export default function LocationDetails({ location, onClose }: Props) {
	const navigate = useNavigate();
	const locNameS = print_short(location);
	const locNameL = print_full(location);

	function SeeAvailable() {
		onClose();
		navigate(`/catalogue/${location.id}`);
	}

	return (<>
		<h1>
			{locNameS}
		</h1>
		<h4>{locNameL}</h4>
		<p>
			{location.description}
		</p>
		<button type="button" onClick={SeeAvailable}>See available books</button>
	</>)
}
