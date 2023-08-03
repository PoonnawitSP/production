import { useState } from "react";
import React from 'react';
import './App.css';
import SignIn from "./SignIn";
import Login from './Login';
import { BrowserRouter as Router, Route, Routes, Navigate} from 'react-router-dom';
import { ToastContainer } from "react-toastify";
import CreateNewUser from './CreateNewUser';
import Dashboard from './Dashboard'
import NewProject from './NewProject'
import PrivateRoute from "./PrivateRoute";


function App() {

  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const handleSignIn = () => {
    setIsAuthenticated(true);
  };

  return (
    <div className="App">
     
      <Router>
      <Routes>
        <Route path="/" element={<Navigate replace to="/signIn" />} />
        <Route exact path="/signIn" Component={SignIn}></Route>
        <Route exact path="/login" Component={Login}></Route>
        <Route path="/createNewUser" Component={CreateNewUser}/> 
        <Route path="/dashboard" Component={Dashboard} />
        <Route path="/createNewProject" Component={NewProject}></Route>
      </Routes>
      </Router>

      <ToastContainer 
        position="top-center"
        autoClose={5000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme="dark"/>     
    </div>
  );
}

export default App;
