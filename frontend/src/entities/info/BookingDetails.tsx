import { useNavigate } from "react-router";
import type { Booking } from '../../data/Types';
import { print_full } from '../../data/Local';
import { cancel_remote_booking } from '../../data/Api';

type Props = {
	booking: Booking;
	onClose: () => void;
}

export default function BookDetails({ booking, onClose }: Props) {
	const navigate = useNavigate();
	const locNameL = print_full(booking.location);

	async function CancelBooking() {
		// window.alert(`${booking.id}`)
		if (!window.confirm("Are you sure?")) return;
		try {
			await cancel_remote_booking(booking.id);
		} catch (e) {
			console.error(e);
			return;
		}
		onClose();
		navigate("/bookings", { replace: true });
	}

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
