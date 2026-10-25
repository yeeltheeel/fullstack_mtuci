import type { Book } from '../../data/Types';
import Modal from '../ui/Modal';
import BookIcon from '../../shared/icons/books.png';
import DetailsIcon from '../../shared/icons/menu.png';
import BookDetails from "../info/BookDetails";

type Props = {
	book: Book;
}

export default function BookCard({ book }: Props) {
	const modal = Modal();
	return (
		<div className="card">
			<div className="card_img">
				<img src={BookIcon} />
			</div>
			<div>
				<h2>{book.title}</h2>
				<h4>by {book.author}</h4>
				<p>{book.genre}</p>
			</div>
			<div className="details_button">
				<button onClick={() =>
					modal.open({
						title: book.title,
						body: <BookDetails book={book} />,
					})}>
					<img src={DetailsIcon} alt="Show details" />
				</button>
			</div>
		</div>
	)
}
