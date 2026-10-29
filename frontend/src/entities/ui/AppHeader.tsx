import { Link } from "react-router";
import type{ User } from '../../data/Types';
import BookIcon from '../../shared/icons/book.png';
import DefaultAvatar from '../../shared/icons/bookworm.png';
import UserProfile from '../info/UserProfile';
import Modal from '../ui/Modal';

type Prop = {
	user: User 
}

export default function AppHeader({user}: Prop){
	const logged = (user != null)
	const avatar_url = (logged && user.avatar) ? user.avatar : DefaultAvatar; 
	const modal = Modal();

	return(<>
	 <div className="app_header">
		<div>
			<img className="app_header_logo" src={BookIcon} alt="BookExchange logo" />
		</div>
		<div>
			<h1>BookExchange</h1>
		</div>
		{logged ? (
			<div className="app_header_actions">
				<div className="app_header_actions_img" 
					onClick={() => modal.open({
						body: <UserProfile user={user} onClose={() => modal.close()}/>,
					})}>
					<img src={avatar_url} alt="User" />
				</div>
			</div>
		):(
			<div className="app_header_actions">
				<Link to="/login">Login</Link>
				<Link to="/register">Register</Link>
			</div>
		)}
	 </div>
	 <div className="navbar">
		<Link to="/">Home</Link>
		<Link to="/catalogue">Catalogue</Link>
		<Link to="/locations">Locations</Link>
		{logged &&
			<Link to="/bookings">My Bookings</Link>
		}
	 </div>
	</>)
}