import type { Book } from '../data/Types';
import BookCard from "../components/BookCard";
import NoContentCard from "../components/NoContentCard";

import { test_books } from "../data/MockData";

type Prop = {
	books: Array<Book>;
}

export default function CataloguePage({ books }: Prop) {
	return (
		<div className="list_display">
			<h1>Catalogue</h1>
			{test_books.length > 0 ? (
				test_books.map((book) => (
					<BookCard book={book} key={book.id} />
				))
			) : (
				<NoContentCard />
			)}
		</div>
	)
}