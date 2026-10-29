import type { Location } from '../../data/Types';
import { useNavigate } from 'react-router';

type Props = {
	location: Location;
	onClose: () => void;
}

export default function LocationDetails({location, onClose}: Props){
	const navigate = useNavigate();

	function SeeAvailable(){
		onClose();
		navigate(`/catalogue/${location.id}`);
	}

	return(<>
	<h1> 
		{location.street}, {location.house}
	</h1>
	<h4>{location.country}, {location.city}, {location.street}, {location.house}</h4>
	<p>
		{location.description}
	</p>
	<button type="button" onClick={SeeAvailable}>See available books</button>
	</>) 
}
