export type User = {
	id: number;
	username: string;
	birthday?: string;
	email: string;
	avatar?: string | null;
}

export type Book = {
	id: number;
	title: string;
	author: string;
	genre: string;
	description: string;
	available: Array<number>;
	locations: Array<Location>;
} 

export type Location = {
	id: number;
	country: string;
	city: string;
	street: string;
	house: string;
	description: string;
}

export type Booking = {
	id: number;
	user: User;
	location: Location;
	book: Book;
	time_created: Date;
	time_due: Date;
	time_closed: Date;
	status: string;
}