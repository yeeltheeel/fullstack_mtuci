import { createBrowserRouter } from "react-router";

import App from "./App";
import HomePage from "./pages/Home";
import CataloguePage from "./pages/Catalogue";
import LocationsPage from "./pages/Locations";
import BookingsPage from "./pages/Bookings";
import LoginPage from "./pages/Login";
import RegisterPage from "./pages/Register";
import NotFoundPage from "./pages/NotFound";

export const router = createBrowserRouter([
  {
    path: "/",
    Component: App,
    children: [
      {
        index: true,
        Component: HomePage,
      },
      {
        path: "catalogue",
        Component: CataloguePage,
      },
      {
        path: "locations",
        Component: LocationsPage,
      },
      {
        path: "bookings",
        Component: BookingsPage,
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
        path: "*",
        Component: NotFoundPage,
      },
    ],
  },
]);