import { useRouteLoaderData } from "react-router";
import { useState } from 'react';
import type { User } from '../../data/Types';

export default function ChangePasswordPage() {
	const { user } = useRouteLoaderData("root") as { user: User | null };
	const password = "none"; // user.get_password() from server
	const [new_password, setNewPassword] = useState('');
	const [confirm, setConfirmPassword] = useState("");

	const passValid = password.length > 4
	const passwordsMatch = password === confirm;
	const confirmValid = confirm.length > 0 && passwordsMatch;
	const formValid = passValid && confirmValid;

	function handleSubmit(e: React.SubmitEvent<HTMLFormElement>) {
		e.preventDefault();
		if (!formValid) {
			if (!passValid)
				window.alert(`invalid password`)
			else if (!confirmValid)
				window.alert(`passwords do not match`)
			return;
		}
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
						minLength={4}
						maxLength={10}
						onChange={e => setNewPassword(e.target.value)}
					/>
				</label>
				<label>
					Confirm new password
					<input
						type="password"
						placeholder="****"
						value={confirm}
						onChange={e => setConfirmPassword(e.target.value)}
					/>
				</label>
				<button type="submit">Change</button>
			</form>
		</div>
	)
}
