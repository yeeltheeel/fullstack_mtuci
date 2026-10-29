import { useRouteLoaderData } from "react-router";
import { useState } from "react";
import type { Book, User } from '../../data/Types';

type Props = {
	book: Book;
	onClose: () => void;
}

export default function BookDetails({book, onClose}: Props){
	const { user } = useRouteLoaderData("root") as { user: User | null };
	const [selectedLocationId, setSelectedLocationId] = useState<number | null>(null);
	const selectedLocation = book.locations.find((l) => l.id === selectedLocationId) ?? null;

	function isLoggedIn(user: User | null): user is User {
		return user !== null;
	}
	
	function handleNewBooking() {
		if (!isLoggedIn(user)) {
			window.alert("Log in or register first");
			return;
		}
		if (!selectedLocation) {
			window.alert("Pick a location first");
			return;
		}
		window.alert(`Booked ${book.title} at ${selectedLocation.city}`);
		onClose();
	} 

	return(<>
	<h1>{book.title}</h1>
	<h2>by {book.author}</h2>
	<h4>{book.genre}</h4>
	<p>
		{book.description}
	</p>
	<h3>Available locations:</h3>
	<ul>
		{book.locations.map((location) => {
			const isSelected = location.id === selectedLocationId;
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
					<span>({book.available} copies)</span>
				</label>
				</li>
			);
		})}
	</ul>
	<button type="button" onClick={handleNewBooking}>Book it</button>
	</>) 
}
