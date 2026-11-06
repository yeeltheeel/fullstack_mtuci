import type { Location} from "./Types";

/* date handling
		date to string: .toISOString().split('T')[0]
		new Date(Date.UTC(2002, 1-1, 3)), // utc for consistency
*/

export function format_date(iso: string | null | undefined): string {
	if (!iso) return '';
	const date = new Date(iso);
	if (Number.isNaN(date.getTime())) 
		return '???';

	const pad = (n: number) => String(n).padStart(2, '0');
	const yyyy = date.getFullYear();
	const mm = pad(date.getMonth() + 1);
	const dd = pad(date.getDate());
	const hh = pad(date.getHours());
	const mi = pad(date.getMinutes());
	const ss = pad(date.getSeconds());
	return `${yyyy}-${mm}-${dd} ${hh}:${mi}:${ss}`;
}

export function format_date_short(iso: string | null | undefined): string {
	if (!iso) return '';
	const date = new Date(iso);
	if (Number.isNaN(date.getTime())) 
		return '???';

	const pad = (n: number) => String(n).padStart(2, '0');
	const yyyy = date.getFullYear();
	const mm = pad(date.getMonth() + 1);
	const dd = pad(date.getDate());
	return `${yyyy}-${mm}-${dd}`;
}

export function print_full(location: Location | null = null): string {
	return location ? location.country + ", " + location.city + ", " + location.street + ", " + location.house : ""
}

export function print_short(location: Location | null = null): string {
	return location ? location.street + ", " + location.house : ""
}