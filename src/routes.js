import React from "react";
import { Redirect } from "react-router-dom";

// Layout Types
import { DefaultLayout } from "./layouts";

// Route Views
import Dashboard from "./views/Dashboard";
import UserProfileLite from "./views/UserProfileLite";
import Messages from "./views/Messages";
import MyPatients from "./views/MyPatients";

export default [
  {
    path: "/",
    exact: true,
    layout: DefaultLayout,
    component: () => <Redirect to="/dashboard" />
  },
  {
    path: "/dashboard",
    layout: DefaultLayout,
    component: Dashboard
  },
  {
    path: "/mypatients",
    layout: DefaultLayout,
    component: MyPatients
  },
  {
    path: "/messages",
    layout: DefaultLayout,
    component: Messages
  },
  {
    path: "/user-profile",
    layout: DefaultLayout,
    component: UserProfileLite
  }
];
