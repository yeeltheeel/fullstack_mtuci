import { useState } from 'react';
import { Link, useNavigate } from 'react-router';

export default function LoginPage(){
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    function handleSubmit(e: React.FormEvent) {
        e.preventDefault();
        console.log('login', { email, password });
        navigate('/');
    }
    
    return(
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