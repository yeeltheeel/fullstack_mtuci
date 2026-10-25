import { useRouteLoaderData } from "react-router";
import LandingImage from '../../shared/images/exchange.jpg';
import type{ User } from '../../data/Types';

export default function HomePage(){
	const { user } = useRouteLoaderData("root") as { user: User | null };
	const logged = (user != null)
	return(
		<div className="list_display">
			<h1>Welcome, {logged ? (user.username):("avid bookworm")}</h1>
			<img src={LandingImage} alt="Welcome"/>
		</div>
	)
}