import type { Book } from '../data/Types';
import Modal from '../components/Modal';
import BookDetails from "../components/BookDetails";
import BookIcon from '../assets/books.png';
import DetailsIcon from '../assets/menu.png';

type Props = {
    book: Book;
}

export default function BookCard({book}: Props){
    const modal = Modal();
    return(
    <div className="card">
        <div className="card_img">
            <img src={BookIcon} />
        </div>
        <div>
            <h2>{book.title}</h2>
            <h4> by {book.author}</h4>
            <p>{book.genre}</p>
        </div>
        <div className="details_button">   
            <button onClick={() =>
                modal.open({
                  title: book.title,
                  body: <BookDetails book={book} />,
                })}>
                <img src={DetailsIcon} alt="Delete booking" />
            </button>
        </div>
    </div>
    ) 
}
