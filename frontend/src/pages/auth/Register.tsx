import { useState } from 'react';
import { Link, useNavigate } from 'react-router';

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export default function RegisterPage() {
	const navigate = useNavigate();
	const [username, setUsername] = useState('');
	const [email, setEmail] = useState('');
	const [birthday, setBirthday] = useState('');
	const [password, setPassword] = useState('');
	const [confirm, setConfirm] = useState('');

	const inputValid = email.length > 0 && password.length > 0
	const emailValid = EMAIL_RE.test(email.trim());
	const passValid = password.length > 4
	const passwordsMatch = password === confirm;
	const confirmValid = confirm.length > 0 && passwordsMatch;
	const formValid = inputValid && emailValid && passValid && confirmValid;

	function handleSubmit(e: React.SubmitEvent<HTMLFormElement>) {
		e.preventDefault();
		if (!formValid) {
			if (!inputValid)
				window.alert(`no input`)
			else if (!emailValid)
				window.alert(`incorrect email`)
			else if (!passValid)
				window.alert(`invalid password`)
			else if (!confirmValid)
				window.alert(`passwords do not match`)
			return;
		}
		window.alert(`register: ${username}, ${email}, ${birthday}, ${password}, ${confirm}`)
		navigate('/');
	}

	return (
		<div className='auth_block'>
			<h1>Registration</h1>
			<form onSubmit={handleSubmit}>
				<label>
					Username
					<input
						type="text"
						placeholder="avid bookworm"
						value={username}
						minLength={1}
						onChange={e => setUsername(e.target.value)}
					/>
				</label>
				<label>
					Email
					<input
						type="email"
						placeholder="book@exchange.org"
						value={email}
						onChange={e => setEmail(e.target.value)}
					/>
				</label>
				<label>
					Birthday
					<input
						type="date"
						value={birthday}
						onChange={e => setBirthday(e.target.value)}
					/>
				</label>
				<label>
					Password
					<input
						type="password"
						placeholder="****"
						value={password}
						minLength={4}
						maxLength={10}
						onChange={e => setPassword(e.target.value)}
					/>
				</label>
				<label>
					Confirm password
					<input
						type="password"
						placeholder="****"
						value={confirm}
						minLength={4}
						maxLength={10}
						onChange={e => setConfirm(e.target.value)}
					/>
				</label>
				<button type="submit">Create account</button>
			</form>
			<p>
				Already have an account? <Link to="/login">Login</Link>
			</p>
		</div>
	)
}