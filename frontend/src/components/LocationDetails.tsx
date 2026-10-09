import type { Location } from '../data/Types';
import Modal from './Modal';

type Props = {
    location: Location;
}

export default function LocationDetails({location}: Props){
    const {close} = Modal();
    return(<>
    <h1> 
        {location.street}, {location.house}
    </h1>
    <h4>{location.country}, {location.city}</h4>
    <p>
        {location.description}
    </p>
    <button onClick={close}>Close</button>
    </>) 
}
