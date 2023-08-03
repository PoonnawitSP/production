import React from "react";
import { Route, Navigate } from "react-router-dom";

const PrivateRoute = ({isAuthenticated, component : Login}) => {
  return (
    <Route
      
      render={({ location }) =>
        isAuthenticated ? (
          <Login />
        ) : (
          <Navigate
            to={{
              pathname: "/signIn",
              state: { from: location },
            }}
          />
        )
      }
    />
  );
};

export default PrivateRoute;
