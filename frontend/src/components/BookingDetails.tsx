import type { Booking } from '../data/Types';

type Props = {
    booking: Booking;
}

export default function BookDetails({booking}: Props){
    return(<>
    <h1>{booking.book.title}</h1>
    <h2>by {booking.book.author}</h2>
    <h2>Status: {booking.status}</h2>
    <h4>
        {booking.time_created.toISOString().split('T')[0]} to {booking.time_due.toISOString().split('T')[0]}
    </h4>
    <h4>{booking.book.genre}</h4>
    <p>
        {booking.book.description}
    </p>
    <button>Delete booking</button>
    </>) 
}
