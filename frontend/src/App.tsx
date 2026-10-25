import { Outlet, useLoaderData } from 'react-router';
import { ModalProvider } from './entities/ui/Modal';
import AppHeader from './entities/ui/AppHeader'
import type { User } from './data/Types';

function App() {
  const { user } = useLoaderData() as { user: User };
  return (<>
	<ModalProvider>
		<AppHeader user={user}/>
		<div className="main_body">
			<Outlet  />
		</div>
	</ModalProvider>
  </>)
}

export default App
