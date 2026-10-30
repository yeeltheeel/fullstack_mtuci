import type { User, Book, Location, Booking } from "./Types";
import { test_user, test_books, test_locations, test_bookings } from "./MockData";

const BACKEND_URL = 'https://localhost:8080'

export async function api<T>(path: string, init?: RequestInit): Promise<T> {
	const url = new URL(path, BACKEND_URL)
	const res = await fetch(url, {
		headers: { 'Content-Type': 'application/json', ...init?.headers },
		...init,
	})
	if (!res.ok) throw new Error(`${res.status} ${res.statusText}`)
	return res.json() as Promise<T>
}
// await api('/auth/login', { method: 'POST', body: JSON.stringify(creds) })

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

export async function fetch_location(locationId: string): Promise<Location> {
	const id = Number(locationId);
	if (!Number.isFinite(id)) {
		throw new Error(`Invalid location id: ${locationId}`);
	}
	const location = test_locations.find((l) => l.id === id); // fetch from server
	if (!location) {
		throw new Error(`Location not found: ${id}`);
	}
	return location;
}

export async function update_remote_user() {
	console.log(`sent user`); // post to server, process response
}
