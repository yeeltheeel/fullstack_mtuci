import LandingImage from '../assets/exchange.jpg';
// import type{ User } from '../data/Types';

import { test_user } from '../data/MockData';

export default function HomePage(){
    const user = test_user;
    return(
        <div>
            <h1>Welcome, {user.logged ? (user.username):("avid bookworm")}</h1>
            <img src={LandingImage} alt="Welcome"/>
        </div>
    )
}