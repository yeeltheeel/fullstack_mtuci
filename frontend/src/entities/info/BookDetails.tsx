import { useRouteLoaderData } from "react-router";
import { useState } from "react";
import type { Book, User } from '../../data/Types';
import { create_booking } from '../../data/Api';
import { print_short } from "../../data/Local";

type Props = {
	book: Book;
	onClose: () => void;
}

export default function BookDetails({ book, onClose }: Props) {
	const { user } = useRouteLoaderData("root") as { user: User | null };
	const [selectedLocationId, setSelectedLocationId] = useState<number | null>(null);
	const selectedLocation = book.locations.find((l) => l.id === selectedLocationId) ?? null;

	function isLoggedIn(user: User | null): user is User {
		return user !== null;
	}

	async function handleNewBooking() {
		if (!isLoggedIn(user)) {
			window.alert("Log in or register first");
			return;
		}
		if (!selectedLocation) {
			window.alert("Pick a location first");
			return;
		}
		await create_booking({
			book_id: book.id,
			loc_id: selectedLocation.id,
			due_days: 14,
		});
		window.alert(`Booked ${book.title} at ${print_short(selectedLocation)}`);
		onClose();
	}

	return (<>
		<h1>{book.title}</h1>
		<h2>by {book.author}</h2>
		<h4>{book.genre}</h4>
		<p>
			{book.description}
		</p>
		<h3>Available locations:</h3>
		<ul>
			{book.locations.map((location, i) => {
				const isSelected = location.id === selectedLocationId;
				const copies = book.available[i] ?? 0;
				return (
					<li key={location.id}>
						<label>
							<input
								type="radio"
								name="location"
								value={location.id}
								checked={isSelected}
								onChange={() => setSelectedLocationId(location.id)}
							/>
							{location.country}, {location.city}, {location.street}, {location.house}{" "}
							<span>({copies} copies)</span>
						</label>
					</li>
				);
			})}
		</ul>
		<button type="button" onClick={handleNewBooking}>Book it</button>
	</>)
}
