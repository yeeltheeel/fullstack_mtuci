import type { User, Book, Location, Booking } from "./Types";
import type { UserOut, LocationOut, BookOut, BookFullDto, BookingOut, TokenPair } from "./Dto";
import { mapUserOut, mapLocationOut, mapBookOut, mapBookFull, mapBookingOut } from "./Mappers";

import { test_user, test_books, test_locations, test_bookings } from "./MockData";

// client

const BACKEND_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8080";

export class ApiError extends Error {
	status: number;
	body: unknown;
	constructor(status: number, body: unknown) {
		super(`${status} ${typeof body === "string" ? body : JSON.stringify(body)}`);
		this.name = "ApiError";
		this.status = status;
		this.body = body;
	}
}

const ACCESS_KEY = "access_token";
const REFRESH_KEY = "refresh_token";

export const tokens = {
	get access() { return localStorage.getItem(ACCESS_KEY); },
	get refresh() { return localStorage.getItem(REFRESH_KEY); },
	set(access: string, refresh: string) {
		localStorage.setItem(ACCESS_KEY, access);
		localStorage.setItem(REFRESH_KEY, refresh);
		},
	clear() {
		localStorage.removeItem(ACCESS_KEY);
		localStorage.removeItem(REFRESH_KEY);
	},
	expiredOrNear(skewMs = 30_000): boolean {
		const a = this.access;
		if (!a) 
			return true;
		try {
			const payload = JSON.parse(atob(a.split(".")[1].replace(/-/g, "+").replace(/_/g, "/")));
			return payload.exp * 1000 - Date.now() < skewMs;
		} catch {
			return true;
		}
	},
};

let refreshing: Promise<void> | null = null;

async function doRefresh(): Promise<void> {
	const refresh_token = tokens.refresh;
	if (!refresh_token) 
		throw new ApiError(401, "No refresh token");

	const res = await fetch(`${BACKEND_URL}/auth/refresh`, {
		method: "POST",
		headers: { "Content-Type": "application/json" },
		body: JSON.stringify({ refresh_token }),
	});
	if (!res.ok) {
		tokens.clear();
		throw new ApiError(401, "Refresh failed");
	}
	const pair = (await res.json()) as TokenPair;
	tokens.set(pair.access_token, pair.refresh_token);
}

function ensureFreshAccess(): Promise<void> {
	if (!tokens.expiredOrNear()) 
		return Promise.resolve();
	if (!refreshing) refreshing = doRefresh().finally(() => { 
		refreshing = null; 
	});
	return refreshing;
}

type Options = RequestInit & { skipAuth?: boolean; _retried?: boolean };

export async function api<T>(path: string, init?: Options): Promise<T> {
	const { skipAuth, _retried, ...rest } = init ?? {};

	if (!skipAuth) 
		await ensureFreshAccess();

	const token = skipAuth ? null : tokens.access;
	const res = await fetch(`${BACKEND_URL}${path}`, {
		...rest,
		headers: {
			"Content-Type": "application/json",
			...(token ? { Authorization: `Bearer ${token}` } : {}),
			...rest.headers,
		},
	});

	// reactive retry — clock skew or another tab rotated already
	if (res.status === 401 && !skipAuth && !_retried) {
		tokens.clear();
		await doRefresh().catch(() => {});
		return api<T>(path, { ...init, _retried: true });
	}

	if (!res.ok) {
		const body = await res.json().catch(() => res.statusText);
		throw new ApiError(res.status, body);
	}
	if (res.status === 204) 
		return undefined as T;
	return res.json() as Promise<T>;
}

// api auth

export async function login(username: string, password: string): Promise<void> {
	const body = new URLSearchParams({ username, password });
	const pair = await api<TokenPair>("/auth/login", {
		method: "POST",
		headers: { "Content-Type": "application/x-www-form-urlencoded" },
		body,
		skipAuth: true,
	});
	tokens.set(pair.access_token, pair.refresh_token);
}

export async function register(input: {
	username: string;
	email: string;
	password: string;
	birthday?: string;
}): Promise<User> {
	const out = await api<UserOut>("/auth/register", {
		method: "POST",
		body: JSON.stringify(input),
		skipAuth: true,
	});
	return mapUserOut(out);
}

export function logout(): void {
	tokens.clear();
}

// api user

export async function load_remote_user(userId: string | null = null): Promise<User | null> {
	const path = userId ? `/users/${Number(userId)}` : "/users/me";
	try {
		return mapUserOut(await api<UserOut>(path));
	} catch (e) {
		if (e instanceof ApiError && (e.status === 401 || e.status === 404)) 
			return null;
		throw e;
	}
}

export async function update_remote_user(input: {
	username?: string;
	email?: string;
	birthday?: string;
	avatar?: string;
}): Promise<User> {
	return mapUserOut(
		await api<UserOut>("/users/me", {
			method: "PATCH",
			body: JSON.stringify(input),
		}),
	);
}

export async function update_remote_password(
	currentPassword: string,
	newPassword: string,
): Promise<void> {
	await api<void>("/users/me/password", {
		method: "PATCH",
		body: JSON.stringify({
			current_password: currentPassword,
			new_password: newPassword,
		}),
	});
}

export async function delete_remote_user(): Promise<void> {
	await api<void>("/users/me", { method: "DELETE" });
	tokens.clear();
}

// api books

export async function load_remote_books(locationId: string | null = null): Promise<Book[]> {
	const books = (await api<BookFullDto[]>("/books/me")).map(mapBookFull);
	if (!locationId) 
		return books;
	const locId = Number(locationId);
	return books.filter((b) => b.available.includes(locId));
}

// api locations

export async function load_remote_locations(): Promise<Location[]> {
	const locations = (await api<LocationOut[]>("/locations/me")).map(mapLocationOut);
	return locations;
}

export async function fetch_location(locationId: string): Promise<Location> {
	const id = Number(locationId);
	if (!Number.isFinite(id)) {
		throw new Error(`Invalid location id: ${locationId}`);
	}
	if (!Number.isFinite(id)) 
		throw new Error(`Invalid location id: ${locationId}`);
	const location = mapLocationOut(await api<LocationOut>(`/locations/${id}`));
	return location;
}

// api bookings

export async function load_remote_bookings(userId: string | null = null): Promise<Booking[]> {
	const bookings = (await api<BookingOut[]>("/bookings/me")).map(mapBookingOut);
	return userId ? bookings.filter((b) => String(b.user.id) === userId) : bookings;
}

export async function create_booking(input: {
	book_id: number;
	loc_id: number;
	due_days: number;
}): Promise<Booking> {
	return mapBookingOut(
		await api<BookingOut>("/bookings", {
			method: "POST",
			body: JSON.stringify(input),
		}),
	);
}

export async function delete_remote_booking(
	bookingId: number
){
	await api<void>(`/bookings/${bookingId}`, { method: "DELETE" });
}
