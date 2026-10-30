import type { User, Book, Location, Booking } from "./Types";

/* date handling
		date to string: .toISOString().split('T')[0]
		new Date(Date.UTC(2002, 1-1, 3)), // utc for consistency
*/

export function print_full(location: Location | null = null): string {
	return location ? location.country + ", " + location.city + ", " + location.street + ", " + location.house : ""
}

export function print_short(location: Location | null = null): string {
	return location ? location.street + ", " + location.house : ""
}