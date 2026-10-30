import type { Booking } from '../../data/Types';
import { print_full } from '../../data/Local';

type Props = {
	booking: Booking;
	onClose: () => void;
}

export default function BookDetails({ booking, onClose }: Props) {
	function CancelBooking() {
		window.alert(`${booking.id}`)
		// remove_booking(booking);
		onClose();
	}
	const locNameL = print_full(booking.location);

	return (<>
		<h1>{booking.book.title}</h1>
		<h2>by {booking.book.author}</h2>
		<h2>Status: {booking.status}</h2>
		<h4>
			{booking.time_created} to {booking.time_due}
			<p>{locNameL}</p>
		</h4>
		<h4>{booking.book.genre}</h4>
		<p>
			{booking.book.description}
		</p>
		{(
			booking.status != "closed" &&
			booking.status != "cancelled") && (
				<button type="button" onClick={CancelBooking}>Cancel booking</button>
			)}
	</>)
}
