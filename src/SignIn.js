import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import 'react-toastify/dist/ReactToastify.css';
import { Link } from 'react-router-dom';
import './page.css'


const SignIn = ({onSignIn}) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
 
  const navigate = useNavigate();

  const handleEmailChange = (event) => {
    setEmail(event.target.value);
  };

  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
  };


  const handleLogin = async (e) => {
    e.preventDefault();

    if(email.trim() === "" || password.trim() === ""){
      alert("Please fill in all fields");
      return;
    }


    const response = await fetch("/signIn", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
    });

    const data = await response.json();
    if(response.status === 200){
        navigate("/login")

    }else{
        toast.error('Invalid userid or password', {position: "top-center", autoClose: 5000, hideProgressBar: false, closeOnClick: true, pauseOnHover: true, draggable: true, progress: undefined, theme: "dark",});
    }
  };

  return (
    <div className = "transbox">
      <div>
      <h1> "The Gadget Groove"</h1><br/>
      <h4>Why Buy when you can Borrow</h4>

      <form onSubmit={handleLogin}>
        <div>
          <label>Email: &ensp;</label>
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required/>*<br/><br/>
        </div>
        <div>
          <label>Password: &ensp;</label>
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required/>*<br/><br/>
        </div>
        <button type="submit">Login</button>
        <div>
          <Link to="/createNewUser">Don't have an account? Signup</Link><br/><br/>
        </div>
        
      </form>
    </div>
    </div>
  );  
};

export default SignIn;