import type { Booking } from '../data/Types';
import BookingCard from "../components/BookingCard";
import { test_bookings } from "../data/MockData";

type Prop = {
    bookings: Array<Booking>;
}

export default function BookingsPage({bookings}: Prop){
    return(
        <div className="list_display">
            <h1>My Bookings</h1>
            {test_bookings.map((booking) => (
                <BookingCard booking={booking} key={booking.id}/>
            ))}
        </div>
    )
}