import type { User } from '../../data/Types';
import DefaultAvatar from '../../shared/icons/bookworm.png';
import { Link, useNavigate } from 'react-router';

type Prop = {
    user: User 
}

export default function UserProfile({user}: Prop){
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
			<label>
				<h4>Birthday</h4>
				{user.birthday}
			</label>
		</div>
	</div>
	
	<button className="user_profile_btn">Edit profile</button> 
	<button className="user_profile_btn">Log out</button>
	<button>Delete account</button>
	</>) 
}