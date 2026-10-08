import type { Booking } from '../data/Types';

type Props = {
    booking: Booking;
}

export default function BookingCard({booking}: Props){
   return(
    <div>
        <div>
            <h1>{booking.book.title} by {booking.book.author} </h1>
            <h2>at {booking.location.street}</h2> {/*location.getAddress()*/}
            <h3>{booking.time_created.toISOString().split('T')[0]} - {booking.time_due.toISOString().split('T')[0]}</h3>
            <h3>Status: {booking.status}</h3>
        </div>
        <div>
            <button>Delete booking</button>
        </div>
    </div>
    ) 
}