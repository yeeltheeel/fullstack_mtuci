import type { User, Book, Location, Booking } from "./Types";

export type UserRow = {
	user_id: number;
	username: string | null;
	birthday: string | Date | null; // pg may return Date or "YYYY-MM-DD"
	email: string;
	avatar_url: string | null;
	password_hash: string;
};

export type BookRow = {
	book_id: number;
	title: string | null;
	author: string | null;
	genre: string | null;
	descr: string | null;
};

export type LocationRow = {
	loc_id: number;
	country: string | null;
	city: string | null;
	street: string | null;
	house: string | null;
	descr: string | null;
};

export type BookingRow = {
	bk_id: number;
	user_id: number;
	book_id: number;
	loc_id: number;
	time_created: Date | string;
	time_due: Date | string | null;
	time_closed: Date | string | null;
	stat: string;
};

export type StockRow = {
	book_id: number;
	loc_id: number;
	available: number;
	reserved: number;
};

const toIso = (v: Date | string): string =>
	v instanceof Date ? v.toISOString() : new Date(v).toISOString();

const toIsoOrNull = (v: Date | string | null): string | null =>
	v == null ? null : toIso(v);

const toDateOnly = (v: Date | string | null): string | undefined => {
	if (v == null) return undefined;
	if (v instanceof Date) return v.toISOString().slice(0, 10);
	return v.slice(0, 10);
};

export const mapUserRow = (row: UserRow): User => ({
	id: row.user_id,
	username: row.username ?? '',
	birthday: toDateOnly(row.birthday),
	email: row.email,
	avatar: row.avatar_url,
});

export const mapLocationRow = (row: LocationRow): Location => ({
	id: row.loc_id,
	country: row.country ?? '',
	city: row.city ?? '',
	street: row.street ?? '',
	house: row.house ?? '',
	description: row.descr ?? '',
});

export type BookWithRelationsRow = BookRow & {
	available_location_ids: number[] | null;
	locations: LocationRow[] | null;
};

export const mapBookRow = (row: BookWithRelationsRow): Book => ({
	id: row.book_id,
	title: row.title ?? '',
	author: row.author ?? '',
	genre: row.genre ?? '',
	description: row.descr ?? '',
	available: row.available_location_ids ?? [],
	locations: (row.locations ?? []).map(mapLocationRow),
});

export type BookingJoinedRow = BookingRow & {
	user: UserRow;
	location: LocationRow;
	book: BookWithRelationsRow;
};

export const mapBookingRow = (row: BookingJoinedRow): Booking => ({
	id: row.bk_id,
	user: mapUserRow(row.user),
	location: mapLocationRow(row.location),
	book: mapBookRow(row.book),
	time_created: toIso(row.time_created),
	time_due: toIsoOrNull(row.time_due),
	time_closed: toIsoOrNull(row.time_closed),
	status: row.stat,
});
