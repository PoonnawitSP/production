import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import 'react-toastify/dist/ReactToastify.css';
import { Link } from 'react-router-dom';
import './prodid.css';

const Login = () => {
  const [projectName, setProjectName] = useState("");
  const [projectId, setProjectId] = useState("");
 
  const navigate = useNavigate();
  const handleLogin = async (e) => {
    e.preventDefault();

    if(projectName.trim() === "" || projectId.trim() === ""){
        alert("Please fill in all fields");
        return;
      }

    const response = await fetch("/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ projectName, projectId }),
    });

    const data = await response.json();
    if(response.status === 200){
      navigate("/dashboard")
    }else if(response.status === 400){
      toast.error('Please login first to create new peoject', {position: "top-center", autoClose: 5000, hideProgressBar: false, closeOnClick: true, pauseOnHover: true, draggable: true, progress: undefined, theme: "dark",});
    }else{
      toast.error('invalid project name or project id', {position: "top-center", autoClose: 5000, hideProgressBar: false, closeOnClick: true, pauseOnHover: true, draggable: true, progress: undefined, theme: "dark",});
    }
  };

  return (
    <div className = "transbox">
    <div>
      <h2>Project Login</h2><br/><br/>
      <form onSubmit={handleLogin}>
        <div>
          <label>Project Name:&ensp;</label>
          <input type="projectName" value={projectName} onChange={(e) => setProjectName(e.target.value)} required />*<br/><br/>
        </div>
        <div>
          <label>Project Id: &ensp; &ensp;</label>
          <input type="projectId" value={projectId} onChange={(e) => setProjectId(e.target.value)} required/>*<br/><br/><br/><br/>
        </div>
        <button type="submit">Join Project</button><br/><br/>
        <div>
          <Link to="/createNewProject">Want to create a new project? Press this</Link>
        </div>
        
      </form>
    </div>
    </div>
    
  );  
};

export default Login;