import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import 'react-toastify/dist/ReactToastify.css';
import { Link } from 'react-router-dom';
import axios from 'axios';
import './proddetails.css'



const Dashboard = ({}) => {
  const [capacity_webcam, setWebcam_Capacity] = useState(null);
  const [capacity_headset, setHeadset_Capacity] = useState(null);
  const [availability_headset, setHeadset_Availability] = useState(null);
  const [availability_webcam, setWebcam_Availability] = useState(null);
  const [headset, setHeadset] = useState("");
  const [webcam, setWebcam] = useState("");
  const [projectId, setprojectId] = useState("");
  const [checkout_headset, setCheckout_headset] = useState("");
  const [checkout_webcam, setCheckout_webcam] = useState("");
  const [members, setMembers] = useState([]);
  const navigate = useNavigate();


  useEffect(() => {
    axios.get('/getWebCam_Capacity')
        .then((response) => setWebcam_Capacity(response.data.value))
        .catch(error => console.log(error));
  }, []);

  
  useEffect(() => {
    axios.get('/getHeadset_Capacity')
        .then((response) => setHeadset_Capacity(response.data.value))
        .catch(error => console.log(error));
  }, []);

  useEffect(() => {
    axios.get('/getWebcam_Availability')
        .then((response) => setWebcam_Availability(response.data.value))
        .catch(error => console.log(error));
  }, []);

  useEffect(() => {
    axios.get('/getHeadset_Availability')
        .then((response) => setHeadset_Availability(response.data.value))
        .catch(error => console.log(error));
  }, []);


  useEffect(() => {
    const fetchDetails = async () => {
      try{
          const response = await fetch("/getdetails");
          const data = await response.json();
          console.log(response)
          console.log(data)
          setprojectId(data.value.projectId)
          setCheckout_headset(data.value.checkout_headset)
          setCheckout_webcam(data.value.checkout_webcam)
      }catch (error) {
        console.error('Error fetching data:', error);
      }
    };
    fetchDetails();
  }, []);


  useEffect(() => {
    const fetchMembers = async () => {
      try{
          const response = await fetch("/getmembers");
          const data = await response.json();
          console.log(response)
          console.log(data)
          setMembers(data)
      }catch (error) {
        console.error('Error fetching members:', error);
      }
    };
    fetchMembers();
  }, []);

  

  const handleInputChange_headset = (event) => {
    const value = event.target.value;

    // Check if the input is a valid whole number
    if (/^\d*$/.test(value)) {
      setHeadset(value);
    }
  };

  const handleInputChange_webcam = (event) => {
    const value = event.target.value;

    // Check if the input is a valid whole number
    if (/^\d*$/.test(value)) {
      setWebcam(value);
    }
  };

  const handleLogout = async (e) => {
    e.preventDefault();
    navigate("/signIn")

    
  };

  const handleCheckout = async (e) => {
    e.preventDefault();

    if(headset.trim() === "" && webcam.trim() === ""){
      alert("No fields requested for checkout");
      return;
    }

    const response = await fetch("/checkout", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ headset, webcam }),
    });

    const data = await response.json();
    if(response.status === 200){
      toast.success('Checkout Succesful', {
        position: "top-right",
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
        theme: "dark",
        });

        console.log(response)
        console.log(data)

        setHeadset_Availability(data.value.headset) 
        setWebcam_Availability(data.value.webcam)
        setCheckout_headset(data.value.checkout_headset)
        setCheckout_webcam(data.value.checkout_webcam)
        setHeadset('')
        setWebcam('')

    }else if(response.status === 500){
      toast.error('You have rquested for more items than available. Please request items within availability', {position: "top-center", autoClose: 5000, hideProgressBar: false, closeOnClick: true, pauseOnHover: true, draggable: true, progress: undefined, theme: "dark",});
    }else if(response.status === 300){
      toast.error('Please login first to checkout', {position: "top-center", autoClose: 5000, hideProgressBar: false, closeOnClick: true, pauseOnHover: true, draggable: true, progress: undefined, theme: "dark",});
    }else {
      toast.error('Error checking out', {position: "top-center", autoClose: 5000, hideProgressBar: false, closeOnClick: true, pauseOnHover: true, draggable: true, progress: undefined, theme: "dark",});
    }
  };


  const handleCheckin = async (e) => {
    e.preventDefault();

    if(headset.trim() === "" && webcam.trim() === ""){
      alert("No fields requested for checkin");
      return;
    }

    const response = await fetch("/checkin", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ headset, webcam }),
    });

    const data = await response.json();
    if(response.status === 200){
      toast.success('Checkin Succesful', {
        position: "top-right",
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
        theme: "dark",
        });

        console.log(response)
        console.log(data)

        setHeadset_Availability(data.value.headset) 
        setWebcam_Availability(data.value.webcam)
        setCheckout_headset(data.value.checkout_headset)
        setCheckout_webcam(data.value.checkout_webcam)
        setHeadset('')
        setWebcam('')

    }else if(response.status === 500){
      toast.error('The field you are requesting to checkin has not been checkedout by your project', {position: "top-center", autoClose: 5000, hideProgressBar: false, closeOnClick: true, pauseOnHover: true, draggable: true, progress: undefined, theme: "dark",});
    }else if(response.status === 300){
      toast.error('Please login first to checkin', {position: "top-center", autoClose: 5000, hideProgressBar: false, closeOnClick: true, pauseOnHover: true, draggable: true, progress: undefined, theme: "dark",});
    }else if(response.status === 400){
      toast.error('You are trying to checkin more than you have checkedout', {position: "top-center", autoClose: 5000, hideProgressBar: false, closeOnClick: true, pauseOnHover: true, draggable: true, progress: undefined, theme: "dark",});
    }else {
      toast.error('Error checking in', {position: "top-center", autoClose: 5000, hideProgressBar: false, closeOnClick: true, pauseOnHover: true, draggable: true, progress: undefined, theme: "dark",});
    }
  };
  
  return (

    <header className ="transbox">
    <div className = "transbox1">
        
      <form>
      <h1>Dashboard</h1> 
      <h5>Project ID : {projectId}</h5><br/>
        <table class ='center'>
          <tr>
            <th></th>
            <th>Capacity</th>
            <th>Availability</th>
            <th>Request</th>
          </tr>
          <tr>
            <th>Head Set</th>
            <td>{capacity_headset}</td>
            <td>{availability_headset}</td>
            <td><input type="text" pattern="[0-9]*" value={headset} onChange={handleInputChange_headset} /></td>
          </tr>
          <tr>
            <th>Web Cam</th>
            <td>{capacity_webcam}</td>
            <td>{availability_webcam}</td>
            <td> <input type="text" pattern="[0-9]*" value={webcam} onChange={handleInputChange_webcam} /></td>
          </tr>
          </table>

        <br/>
            <br/>
        <button type="submit" onClick = {handleCheckout} >Checkout</button>
        <button type="submit" onClick = {handleCheckin} >Checkin</button>
        <button type="submit" onClick = {handleLogout} >logout</button>
        <br/>
        <label> Checked out headset : {checkout_headset}</label><br/>
        <label> Checked out webcam : {checkout_webcam}</label>
           
        <br/><br/><br/><br/><br/><br/><br/>
        </form>
        </div>


      <div className = 'trans'>
        <br/>
        <h2>Project members </h2>
       

              <ul>
                {members.map((item, index) => (
                  <li key={index}>{item}</li>
                ))}
              </ul>
           
        </div>
        
        
            
    </header>
  );  
};

export default Dashboard;