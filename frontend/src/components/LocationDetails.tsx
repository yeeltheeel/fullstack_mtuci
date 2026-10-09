import type { Location } from '../data/Types';

type Props = {
    location: Location;
}

export default function LocationDetails({location}: Props){
    return(<>
    <h1> 
        {location.street}, {location.house}
    </h1>
    <h4>{location.country}, {location.city}, {location.street}, {location.house}</h4>
    <p>
        {location.description}
    </p>
    <button>See available books</button>
    </>) 
}
