import { useState } from 'react';
import { Link, useNavigate } from 'react-router';

export default function RegisterPage(){
    const navigate = useNavigate();
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [birthday, setBirthday] = useState('');
    const [password, setPassword] = useState('');
    const [confirm, setConfirm] = useState('');

    function handleSubmit(e: React.FormEvent) {
        e.preventDefault();
        console.log('register', { username, email, birthday, password, confirm });
        navigate('/');
    }

    return(
        <div className='auth_block'>
            <h1>Registration</h1>
            <form onSubmit={handleSubmit}>
                <label>
                    Username
                    <input type="text" value={username} onChange={e => setUsername(e.target.value)} />
                </label>
                <label>
                    Email
                    <input type="email" value={email} onChange={e => setEmail(e.target.value)} />
                </label>
                <label>
                    Birthday
                    <input type="date" value={birthday} onChange={e => setBirthday(e.target.value)} />
                </label>
                <label>
                    Password
                    <input type="password" value={password} onChange={e => setPassword(e.target.value)} />
                </label>
                <label>
                    Confirm password
                    <input type="password" value={confirm} onChange={e => setConfirm(e.target.value)} />
                </label>
                <button type="submit">Create account</button>
            </form>
            <p>
                Already have an account? <Link to="/login">Login</Link>
            </p>
        </div>
    )
}