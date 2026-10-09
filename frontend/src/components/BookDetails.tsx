import type { Book } from '../data/Types';
import Modal from './Modal';

type Props = {
    book: Book;
}

export default function BookDetails({book}: Props){
    const {close} = Modal();

    return(<>
    <h1>{book.title}</h1>
    <h1>by {book.author}</h1>
    <h4>{book.genre}</h4>
    <p>
        {book.description}
    </p>
    <h3>Available locations:</h3>
    <ul>
        {book.locations.map((location) => (
            <li key={location.id}>
                {location.country}, 
                {location.city}, 
                {location.street}, 
                {location.house}
            </li>
        ))}
    </ul>
    <button>Book here</button>
    </>) 
}
