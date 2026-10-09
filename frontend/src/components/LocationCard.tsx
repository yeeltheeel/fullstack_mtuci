import type { Location } from '../data/Types';
import Modal from '../components/Modal';
import LocationIcon from '../assets/university.png';
import LocationDetails from "../components/LocationDetails";
import DetailsIcon from '../assets/ellipsis.png';

type Props = {
    location: Location;
}

export default function LocationCard({location}: Props){
    const modal = Modal();
    return(
    <div className="card">
        <div className="card_img">
            <img src={LocationIcon} />
        </div>
        <h2>{location.country}, {location.city}, {location.street}, {location.house}</h2>
        <div className="details_button">   
            <button onClick={() =>
                modal.open({
                    body: <LocationDetails location={location} />,
                })}>
                <img src={DetailsIcon} alt="Delete booking" />
            </button>
        </div>
    </div>
   ) 
}