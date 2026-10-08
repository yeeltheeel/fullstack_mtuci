import type { Book } from '../data/Types';
import BookIcon from '../assets/books.png';
import DetailsIcon from '../assets/ellipsis.png';

type Props = {
    book: Book;
}

export default function BookCard({book}: Props){
   return(
    <div className="card">
        <div className="card_img">
            <img src={BookIcon} />
        </div>
        <div>
            <h2>{book.title}</h2>
            <p>{book.author}</p>
            <p>{book.genre}</p>
        </div>
        <div className="details_button">   
            <button>
                <img src={DetailsIcon} alt="Delete booking" />
            </button>
        </div>
    </div>
    ) 
}
