import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import 'react-toastify/dist/ReactToastify.css';
import './newprod.css'

const NewProject = () => {
  const [projectName, setProjectName] = useState("");
  const [projectId, setProjectId] = useState("");
  const [description, setDescription] = useState("");
 
  const navigate = useNavigate();
  const handleLogin = async (e) => {
    e.preventDefault();

    if(projectName.trim() === "" || projectId.trim() === ""){
        alert("Please fill in all fields");
        return;
      }

    const response = await fetch("/createNewProject", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ projectName, projectId, description }),
    });

    const data = await response.json();
    console.log(response)
    if(response.status === 200){
        navigate("/dashboard")
    }else if(response.status === 500){
        toast.error('Project Id Aready Exists use different Project Id', {position: "top-center", autoClose: 5000, hideProgressBar: false, closeOnClick: true, pauseOnHover: true, draggable: true, progress: undefined, theme: "dark",});
    }else if(response.status === 400){
      toast.error('Please login first to create new peoject', {position: "top-center", autoClose: 5000, hideProgressBar: false, closeOnClick: true, pauseOnHover: true, draggable: true, progress: undefined, theme: "dark",});
    }else{
        toast.error('Error creating project', {position: "top-center", autoClose: 5000, hideProgressBar: false, closeOnClick: true, pauseOnHover: true, draggable: true, progress: undefined, theme: "dark",});
    }
  };

  return (
   <div className = "transbox">
    <div>
      <br/>
      <h2>New Project</h2><br/><br/>
      <form onSubmit={handleLogin}>
        <div>
          <label>Project Name:&ensp;</label>
          <input type="name" value={projectName} onChange={(e) => setProjectName(e.target.value)} required />*<br/><br/>
        </div>
        <div>
          <label>Project Id: &ensp;&ensp;</label>
          <input type="projectId" value={projectId} onChange={(e) => setProjectId(e.target.value)} required/>*<br/><br/>
        </div>
        <div>
          <label>Project Description: &ensp;&ensp;</label>
          <input type="description" value={description} onChange={(e) => setDescription(e.target.value)}/><br/><br/>
        </div>
        <button type="submit">Create Project</button>
      </form>
    </div>
    </div>
  );  
};

export default NewProject;