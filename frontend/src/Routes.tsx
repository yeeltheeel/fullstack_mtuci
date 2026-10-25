import { createBrowserRouter } from "react-router";
import App from "./App";
import HomePage from "./pages/main/Home";
import CataloguePage from "./pages/main/Catalogue";
import LocationsPage from "./pages/main/Locations";
import BookingsPage from "./pages/main/Bookings";
import LoginPage from "./pages/auth/Login";
import RegisterPage from "./pages/auth/Register";
import NotFoundPage from "./pages/main/NotFound";
import EditProfilePage from "./pages/auth/EditProfile";
import ChangePasswordPage from "./pages/auth/ChangePassword";
import { load_remote_user, load_remote_books, load_remote_locations, load_remote_bookings } from "./data/Api";

export const router = createBrowserRouter([
  {
	path: "/",
	id: "root",
	Component: App,
	loader: async () => ({
		user: await load_remote_user(),
	}),
	shouldRevalidate: ({ currentUrl, nextUrl }) => {
		// no unnecessary reruns
		return currentUrl.pathname !== nextUrl.pathname;
	},
	children: [
	  {
		index: true,
		Component: HomePage,
	  },
	  {
		path: "catalogue",
		Component: CataloguePage, 
		loader: async () => {
			return { books: await load_remote_books() };
		},
	  },
	  {
		path: "locations",
		Component: LocationsPage,
		loader: async() => {
			return { locations: await load_remote_locations() }
		}
	  },
	  {
		path: "bookings",
		Component: BookingsPage,
		loader: async() => {
			return { bookings: await load_remote_bookings() }
		}
	  },
	  {
		path: "*",
		Component: NotFoundPage,
	  },
	  {
		path: "login",
		Component: LoginPage,
	  },
	  {
		path: "register",
		Component: RegisterPage,
	  },
	  {
		path: "edit",
		Component: EditProfilePage
	  },
	  {
		path: "password",
		Component: ChangePasswordPage,
	  },
	],
  },
]);