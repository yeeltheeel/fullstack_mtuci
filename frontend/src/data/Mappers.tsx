import type { User, Book, Location, Booking } from "./Types";

import type {
	UserOut,
	BookOut,
	BookFullDto,
	LocationOut,
	BookingOut
} from "./Dto";

export const mapUserOut = (u: UserOut): User => ({
	id: u.user_id,
	username: u.username ?? "",
	birthday: u.birthday ?? undefined,
	email: u.email,
	avatar: u.avatar
});

export const mapLocationOut = (l: LocationOut): Location => ({
	id: l.loc_id,
	country: l.country ?? "",
	city: l.city ?? "",
	street: l.street ?? "",
	house: l.house ?? "",
	description: l.descr ?? ""
});

export const mapBookOut = (b: BookOut): Book => ({
	id: b.book_id,
	title: b.title ?? "",
	author: b.author ?? "",
	genre: b.genre ?? "",
	description: b.descr ?? "",
	available: [],
	locations: []
});

export const mapBookFull = (b: BookFullDto): Book => ({
	id: b.book_id,
	title: b.title ?? "",
	author: b.author ?? "",
	genre: b.genre ?? "",
	description: b.descr ?? "",
	available: b.available,
	locations: b.locations.map(mapLocationOut)
});

export const mapBookingOut = (b: BookingOut): Booking => ({
	id: b.bk_id,
	user: mapUserOut(b.user),
	book: mapBookOut(b.book),
	location: mapLocationOut(b.location),
	time_created: b.time_created,
	time_due: b.time_due,
	time_closed: b.time_closed,
	status: b.stat
});
