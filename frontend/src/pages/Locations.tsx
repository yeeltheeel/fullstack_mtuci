import LocationCard from "../components/LocationCard";
import { test_locations } from "../data/MockData";

export default function LocationsPage(){
    return(
        <div className="list_display">
            <h1>Our Locations</h1>
            {test_locations.map((location) => (
                <LocationCard location={location} key={location.id}/>
            ))}
        </div>
    )
}