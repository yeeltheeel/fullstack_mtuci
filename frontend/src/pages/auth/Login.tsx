import { useState } from 'react';
import { Link, useNavigate } from 'react-router';

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export default function LoginPage() {
	const navigate = useNavigate();
	const [email, setEmail] = useState('');
	const [password, setPassword] = useState('');

	const inputValid = email.length > 0 && password.length > 0
	const emailValid = EMAIL_RE.test(email.trim());
	const passValid = password.length > 4
	const formValid = inputValid && emailValid && passValid;

	function handleSubmit(e: React.SubmitEvent<HTMLFormElement>) {
		e.preventDefault();
		if (!formValid) {
			if (!inputValid)
				window.alert(`no input`)
			else if (!emailValid)
				window.alert(`incorrect email`)
			else if (!passValid)
				window.alert(`invalid password`)
			return;
		}
		window.alert(`login: ${email}, ${password}`)
		navigate('/');
	}

	return (
		<div className='auth_block'>
			<h1>Login</h1>
			<form onSubmit={handleSubmit}>
				<label>
					Email
					<input
						type="email"
						value={email}
						onChange={e => setEmail(e.target.value)}
					/>
				</label>
				<label>
					Password
					<input
						type="password"
						value={password}
						minLength={4}
						maxLength={10}
						onChange={e => setPassword(e.target.value)}
					/>
				</label>
				<button type="submit">Login</button>
			</form>
			<p>
				No account? <Link to="/register">Register</Link>
			</p>
		</div>
	)
}