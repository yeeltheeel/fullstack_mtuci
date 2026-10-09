// import './App.css'
import { Outlet } from 'react-router';
import AppHeader from './components/AppHeader'

import { test_user } from './data/MockData';

function App() {
  return (<>
    <AppHeader user={test_user} />
    <div className="main_body">
      <Outlet  />
    </div>
  </>)
}

export default App
