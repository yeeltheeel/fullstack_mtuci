// mirror app/schemas/*.py

export type UserOut = {
	user_id: number;
	username: string | null;
	email: string;
	birthday: string | null;
	avatar: string | null;
};

export type LocationOut = {
	loc_id: number;
	country: string | null;
	city: string | null;
	street: string | null;
	house: string | null;
	descr: string | null;
};

export type BookOut = {
	book_id: number;
	title: string | null;
	author: string | null;
	genre: string | null;
	descr: string | null;
};

export type BookFullDto = BookOut & {
	available: number[];
	locations: LocationOut[];
};

export type StockOut = {
	book_id: number;
	loc_id: number;
	available: number | null;
	reserved: number | null;
};

export type BookingOut = {
	bk_id: number;
	user: UserOut;
	book: BookOut; 
	location: LocationOut;
	time_created: string; 
	time_due: string | null;
	time_closed: string | null;
	stat: string;
};

export type TokenPair = {
	access_token: string;
	refresh_token: string;
	token_type: string;
};