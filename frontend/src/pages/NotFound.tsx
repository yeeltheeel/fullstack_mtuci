import { Link } from 'react-router';
import travoltaMeme from '../assets/travolta.gif';

export default function BookingsPage(){
    return(
        <div className="list_display">
            <h1>Page not found</h1>
            <img src={travoltaMeme}/>
            <p></p>
            <Link to="/">Back to home</Link>
        </div>
    )
}