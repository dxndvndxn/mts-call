import React from "react";
import ReactDOM from "react-dom/client";
import "antd/dist/reset.css";
import { AppRouting } from "./app";

const root = ReactDOM.createRoot(
  document.getElementById("root") as HTMLElement,
);

root.render(
  // <React.StrictMode>
  <AppRouting />,
  // </React.StrictMode>,
);
