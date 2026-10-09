import type { User } from '../data/Types';
import DefaultAvatar from '../assets/bookworm.png';

type Props = {
    user: User;
}

export default function UserProfile({user}: Props){
    const avatar_url = user.avatar ?? DefaultAvatar; 
    return(<>
    <h1>User profile</h1>
    <div className="user_profile">
        <div className="user_profile_img">
            <img src={avatar_url} />
        </div>
        <div>
            <label>
            <h4>Username</h4>
            {user.username}
        </label>
        <label>
            <h4>Email</h4>
            {user.email}
        </label>
        </div>
    </div>
    <button style={{ marginBottom: -0.6 + 'em' }}>Log out</button>
    <button>Delete account</button>
    </>) 
}