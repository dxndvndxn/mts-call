import { type RouteObject, createBrowserRouter } from "react-router";
import { Operator } from "../../operator";
import { Client } from "../../client";
import { App } from "../App";

export const routes: RouteObject[] = [
  {
    path: "/",
    element: <Operator />,
  },
  {
    path: "/client",
    element: <Client />,
  },
];

export const APP_ROUTER = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: routes.map((route) => ({
      index: route.path === "/",
      path: route.path === "/" ? undefined : route.path,
      element: route.element,
    })),
  },
]);
