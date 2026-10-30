import { useRouteLoaderData } from "react-router";
import { useState } from 'react';
import type { User } from '../../data/Types';

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export default function EditProfilePage(){
    const { user } = useRouteLoaderData("root") as { user: User | null };
    const [username, setUsername] = useState('');
	const [email, setEmail] = useState('');
	const [birthday, setBirthday] = useState('');

	const emailValid = EMAIL_RE.test(email.trim());

    function handleSubmit(e: React.SubmitEvent<HTMLFormElement>) {
		e.preventDefault();
		if (!emailValid){
			if (!emailValid)
				window.alert(`incorrect email`)
			return;
		}
		window.alert(`update: ${username}, ${email}, ${birthday}`)
	}

    return (
        <div className='auth_block'>
			<h1>Edit profile</h1>
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
				<button type="submit">Save</button>
			</form>
        </div>
    )
}
