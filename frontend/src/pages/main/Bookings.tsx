import { useLoaderData } from "react-router";
import type { Booking } from '../../data/Types';
import BookingCard from "../../entities/cards/BookingCard";
import NoContentCard from "../../entities/cards/NoContentCard";

export default function BookingsPage() {
	const { bookings } = useLoaderData() as { bookings: Booking[] }
	return (
		<div className="list_display">
			<h1>My Bookings</h1>
			{bookings.length > 0 ? (
				bookings.map((booking) => (
					<BookingCard booking={booking} key={booking.id} />
				))
			) : (
				<NoContentCard />
			)}
		</div>
	)
}