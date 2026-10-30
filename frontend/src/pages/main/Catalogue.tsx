import { Link, useLoaderData, useParams } from "react-router";
import type { Book } from '../../data/Types';
import BookCard from "../../entities/cards/BookCard";
import NoContentCard from "../../entities/cards/NoContentCard";

export default function CataloguePage() {
	const { books } = useLoaderData() as { books: Book[] };
	const { locationId } = useParams();

	return (
		<div className="list_display">
			<h1>Catalogue</h1>

			{locationId && (
				<div>
					<h2>Books at location # {locationId}</h2>
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