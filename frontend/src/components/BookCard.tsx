import type { Book } from '../data/Types';

type Props = {
    book: Book;
}

export default function BookCard({book}: Props){
   return(
    <div>
        <div>
            <h1>{book.title}</h1>
            <h2>{book.author}</h2>
            <h3>{book.genre}</h3>
        </div>
        <div>
            <button>Details</button>
        </div>
    </div>
    ) 
}
