import type { Booking } from '../../data/Types';
import Modal from '../ui/Modal';
import BookingIcon from '../../shared/icons/diploma.png';
import DetailsIcon from '../../shared/icons/menu.png';
import BookingDetails from "../info/BookingDetails";

type Props = {
    booking: Booking;
}

export default function BookingCard({booking}: Props){
    const modal = Modal();
    return(
    <div className="card">
        <div className="card_img">
            <img src={BookingIcon} />
        </div>
        <div>
            <h2>{booking.book.title}</h2>
            <h4>by {booking.book.author}</h4>
            <p>
                {booking.time_created.toISOString().split('T')[0]} to {booking.time_due.toISOString().split('T')[0]}
            </p>
            <p className="card_status">Status: {booking.status}</p>
        </div>
        <div className="details_button">   
            <button onClick={() =>
                modal.open({
                  body: <BookingDetails booking={booking} />,
                })}>
                <img src={DetailsIcon} alt="Show details" />
            </button>
        </div>
    </div>
    ) 
}