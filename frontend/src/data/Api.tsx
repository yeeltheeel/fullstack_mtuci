import type { User, Book, Location, Booking } from "./Types";
import { test_user, test_books, test_locations, test_bookings } from "./MockData";

/* date handling
		date to string: .toISOString().split('T')[0]
		new Date(Date.UTC(2002, 1-1, 3)), // utc for consistency
*/

export async function load_remote_user(userId: string | null = null): Promise<User | null> {
	const user = test_user; // get from server, process response
	return user;
}

export async function load_remote_books(locationId: string | null = null): Promise<Book[]> {
	const books = locationId
		? test_books.filter((b) =>
			b.locations.some((loc) => String(loc.id) === locationId)
		)
		: test_books;
	return books;
}

export async function load_remote_locations(): Promise<Location[]> {
	const locations = test_locations;
	return locations;
}

export async function load_remote_bookings(): Promise<Booking[]> {
	const bookings = test_bookings;
	return bookings;
}

// export async function fetch_location(locationId: string): Promise<Location[]> {
// 	const location = test_locations[Number(locationId)]; // fetch from server
// 	return location;
// }

export async function update_remote_user() {
	console.log(`sent user`); // post to server, process response
}
