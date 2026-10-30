import { Link, useLoaderData, useParams } from "react-router";
import type { Book, Location } from '../../data/Types';
import BookCard from "../../entities/cards/BookCard";
import NoContentCard from "../../entities/cards/NoContentCard";
import { print_short } from "../../data/Local";

export default function CataloguePage() {
	const { books, location } = useLoaderData() as {
		books: Book[];
		location: Location | null;
	};
	// const { locationId } = useParams();
	const locName = print_short(location);

	return (
		<div className="list_display">
			<h1>Catalogue</h1>

			{location && (
				<div>
					<h2>Available books at {locName}</h2>
					<Link to="/catalogue">Clear filter</Link>
					<div style={{ height: 1 + 'em' }}></div>
				</div>
			)}

			{books.length > 0 ? (
				books.map((book) => (
					<BookCard book={book} key={book.id} />
				))
			) : (
				<NoContentCard />
			)}
		</div>
	)
}