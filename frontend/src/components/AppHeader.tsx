import { Link } from "react-router";
import type{ User } from '../data/Types';

type Prop = {
    user: User;
}

export default function AppHeader({user}: Prop){
    return(<>
     <div>
        <div>
            <img src="../assets/book.png" />
        </div>
        <div>
            <h1>BookExchange</h1>
        </div>
        {/* @if (user.logged) {
            <div>
                <img src="{user.avatar}" />
            </div>
        } else {
            <div>
                <button>Login</button>
                <button>Register</button>
            </div>
        } */}
     </div>
     <div>
        <Link to="/">Home</Link>
     </div>
    </>)
}