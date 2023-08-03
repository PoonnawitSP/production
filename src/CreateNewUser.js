import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import 'react-toastify/dist/ReactToastify.css';
import './page2.css'

const CreateNewUser = () => {
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [preferredName, setPreferredName] = useState("");
  const [email, setEmail] = useState("");
  const [contact, setContact] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
 
  const navigate = useNavigate();
  const handleLogin = async (e) => {
    e.preventDefault();
    
    if(firstName.trim() === "" || email.trim() === "" || password.trim() === "" || confirmPassword.trim() === ""){
      alert("Please fill in all required fields");
      return;
    }

    const response = await fetch("/createNewUser", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ firstName, lastName, preferredName, email, contact, password, confirmPassword}),
    });

    const data = await response.json();
    if(response.status === 200){
        navigate("/login")
    }else if(response.status === 400){
      toast.error('Both the passwords are not matching', {position: "top-center", autoClose: 5000, hideProgressBar: false, closeOnClick: true, pauseOnHover: true, draggable: true, progress: undefined, theme: "dark",});
    }else if(response.status === 500){
      toast.error('Email Id already exists please use another email Id', {position: "top-center", autoClose: 5000, hideProgressBar: false, closeOnClick: true, pauseOnHover: true, draggable: true, progress: undefined, theme: "dark",});
    }else{
        toast.error('Error creating user', {position: "top-center", autoClose: 5000, hideProgressBar: false, closeOnClick: true, pauseOnHover: true, draggable: true, progress: undefined, theme: "dark",});
    }
  };

  return (
    <div className ="transbox2">
    <div>
      <h1>New User</h1>
      <form onSubmit={handleLogin}>
        <div>
          <label>FirstName:</label>
          <input type="firstName" value={firstName} onChange={(e) => setFirstName(e.target.value)} required/>*<br/><br/>
        </div>
        <div>
          <label>LastName:</label>
          <input type="lastName" value={lastName} onChange={(e) => setLastName(e.target.value)} /><br/><br/>
        </div>
        <div>
          <label>PreferredName:</label>
          <input type="preferredName" value={preferredName} onChange={(e) => setPreferredName(e.target.value)} /><br/><br/>
        </div>
        <div>
          <label>Email:</label>
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)}  required/>*<br/><br/>
        </div>
        <div>
          <label>Contact:</label>
          <input type="contact" value={contact} onChange={(e) => setContact(e.target.value)} /><br/><br/>
        </div>
        <div>
          <label>Password:</label>
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required/>*<br/><br/>
        </div>
        <div>
          <label>Confirm Password:</label>
          <input type="password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} required/>*<br/><br/>
        </div>
        <button type="submit"> Create </button>
      </form>
    </div>
    </div>
  );  
};

export default CreateNewUser;