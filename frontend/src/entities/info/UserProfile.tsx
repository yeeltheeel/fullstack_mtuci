import { useState } from 'react';
import { useNavigate } from 'react-router';
import type { User } from '../../data/Types';
import DefaultAvatar from '../../shared/icons/bookworm.png';
import { delete_remote_user, logout, ApiError } from '../../data/Api';

type Prop = {
	user: User;
	onClose: () => void;
}

export default function UserProfile({ user, onClose }: Prop) {
	const navigate = useNavigate();
	const [busy, setBusy] = useState(false);
	const [error, setError] = useState<string | null>(null);

	const avatar_url = user.avatar ?? DefaultAvatar;

	function OpenEditProfile() {
		onClose();
		navigate('/edit');
	}

	function OpenChangePass() {
		onClose();
		navigate('/password');
	}

	function LogOut() {
		onClose();
		logout();
		//navigate('/', { replace: true });
		window.location.href = '/';
	}

	async function DeleteAccount() {
		onClose();
		setBusy(true);
		setError(null);
		try {
			await delete_remote_user();
			navigate('/', { replace: true });
		} catch (err) {
			if (err instanceof ApiError && err.status === 401) {
				setError('Invalid email or password');
			} else {
				setError('Login failed. Try again.');
			}
		} finally {
			setBusy(false);
		}
		window.alert('Successfully deleted')
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
		<button className="user_profile_btn" type="button" onClick={LogOut}>Log out</button>
		<button type="button" onClick={DeleteAccount}>Delete account</button>
	</>)
}