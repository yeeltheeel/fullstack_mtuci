import { useRouteLoaderData } from "react-router";
import { useState } from 'react';
import type { User } from '../../data/Types';

export default function ChangePasswordPage(){
	const { user } = useRouteLoaderData("root") as { user: User | null };
	const password = "none"; // user.get_password() from server
	const [new_password, setNewPassword] = useState('');
	const [confirm_password, setConfirmPassword] = useState("");

	function handleSubmit(e: React.SubmitEvent<HTMLFormElement>){
		e.preventDefault();
		window.alert(`register: ${password}, ${new_password}`)
	}

	return (
		<div className='auth_block'>
			<h1>Change password</h1>
			<form onSubmit={handleSubmit}>
				<label>
					New password
					<input
						type="password"
						placeholder="****"
						value={new_password}
						onChange={e => setNewPassword(e.target.value)}
					/>
				</label>
				<label>
					Confirm new password
					<input
						type="password"
						placeholder="****"
						value={confirm_password}
						onChange={e => setConfirmPassword(e.target.value)}
					/>
				</label>
				<button type="submit">Change</button>
			</form>
		</div>
	)
}
