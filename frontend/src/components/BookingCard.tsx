import type { Booking } from '../data/Types';
import BookingIcon from '../assets/diploma.png';
import DetailsIcon from '../assets/ellipsis.png';

type Props = {
    booking: Booking;
}

export default function BookingCard({booking}: Props){
   return(
    <div className="card">
        <div className="card_img">
            <img src={BookingIcon} />
        </div>
        <div>
            <h2>{booking.book.title} by {booking.book.author} </h2>
            <p>
                {booking.time_created.toISOString().split('T')[0]} to 
                {booking.time_due.toISOString().split('T')[0]}
            </p>
            <p>Status: {booking.status}</p>
        </div>
        <div className="details_button">   
            <button>
                <img src={DetailsIcon} alt="Delete booking" />
            </button>
        </div>
    </div>
    ) 
}