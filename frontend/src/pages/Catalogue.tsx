import BookCard from "../components/BookCard";
import { test_books } from "../data/MockData";

export default function CataloguePage(){
    return(
        <div className="list_display">
            <h1>Catalogue</h1>
            {test_books.map((book) => (
                <BookCard book={book} />
            ))}
        </div>
    )
}