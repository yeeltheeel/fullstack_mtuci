import { useLoaderData } from "react-router";
import type { Book } from '../../data/Types';
import BookCard from "../../entities/cards/BookCard";
import NoContentCard from "../../entities/cards/NoContentCard";

export default function CataloguePage() {
	const { books } = useLoaderData() as { books: Book[] };
	return (
		<div className="list_display">
			<h1>Catalogue</h1>
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