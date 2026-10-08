import { useState } from 'react'
import './App.css'
import AppHeader from './components/AppHeader'

import { test_user } from './data/MockData';

function App() {
  const [count, setCount] = useState(0)

  return (<>
    <AppHeader user={test_user} />
  </>)
}

export default App
