import type { Location } from '../data/Types';
import LocationIcon from '../assets/university.png';
import DetailsIcon from '../assets/ellipsis.png';

type Props = {
    location: Location;
}

export default function LocationCard({location}: Props){
   return(
    <div className="card">
        <div className="card_img">
            <img src={LocationIcon} />
        </div>
        <h2>{location.country}, {location.city}, {location.street}, {location.house}</h2>
        <div className="details_button">   
            <button>
                <img src={DetailsIcon} alt="Delete booking" />
            </button>
        </div>
    </div>
   ) 
}