import type { User, Book, Location, Booking } from './Types';

export const test_user: User = {
    id: 1, 
    username: "Test User",
    birthday: new Date(2000, 9, 1),
    email: "mock@example.com",
    avatar: "",
    logged: true
}