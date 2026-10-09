import type { Booking } from '../data/Types';
import Modal from './Modal';

type Props = {
    booking: Booking;
}

export default function BookDetails({booking}: Props){
    const {close} = Modal();
    return(<>
    <h1>{booking.book.title}</h1>
    <h1>by {booking.book.author}</h1>
    <h2>Status: {booking.status}</h2>
    <h4>
        {booking.time_created.toISOString().split('T')[0]} to {booking.time_closed.toISOString().split('T')[0]}
    </h4>
    <h4>{booking.book.genre}</h4>
    <p>
        {booking.book.description}
    </p>
    <button>Delete booking</button>
    </>) 
}
