// import { useEffect, useState } from 'react';
import type { Book } from '../data/Types';

type Props = {
    book: Book;
}

export default function BookDetails({book}: Props){
    return(
    <div>
        <h1>{book.title} by {book.author}</h1>
        <h2>{book.genre}</h2>
        <p>
            {book.description}
        </p>
        <h3>Available locations:</h3>
        <ul>
            {book.locations.map((location) => (
                <li key={location.id}>
                    {location.country}, {location.city}, {location.street}, {location.house}
                </li>
            ))}
        </ul>
        <button>Book here</button>
    </div>
    ) 
}
