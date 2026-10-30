import type { User } from '../../data/Types';
import DefaultAvatar from '../../shared/icons/bookworm.png';
import { useNavigate } from 'react-router';

type Prop = {
	user: User;
	onClose: () => void;
}

export default function UserProfile({ user, onClose }: Prop) {
	const navigate = useNavigate();
	const avatar_url = user.avatar ?? DefaultAvatar;

	function OpenEditProfile() {
		onClose();
		navigate('/edit');
	}

	function OpenChangePass() {
		onClose();
		navigate('/password');
	}

	return (<>
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

		<button className="user_profile_btn" type="button" onClick={OpenEditProfile}>Edit profile</button>
		<button className="user_profile_btn" type="button" onClick={OpenChangePass}>Change password</button>
		<button className="user_profile_btn" type="button">Log out</button>
		<button type="button">Delete account</button>
	</>)
}