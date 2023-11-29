import Home from "./pages/home";
import Login from './pages/login';
import Signup from './pages/signup';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import {useState} from 'react';

import './App.css';

function App() {
  const [name,setName]=useState('');
  const [age,setAge]=useState('');
  const [gender,setGender]=useState('');
  const [fileimg,setFile]=useState('');
  const [filename,setFilename]=useState('');
  const [uploadedfile,setuploadedfile]=useState({});
  const [downloadfile,setdownloadfile]=useState('');
  const [email,setEmail]=useState('')
  const [password,setPassword]=useState('')   

  return (
    <Router>
        <Routes>
          <Route exact path="/" element={<Login email={email} setEmail={setEmail} password={password} setPassword={setPassword} 
              name={name} setName={setName} age={age} setAge={setAge} gender={gender} setGender={setGender}/>} />
          <Route exact path="/home" element={
              <Home name={name} setname={setName} age={age} setage={setAge} gender={gender} setgender={setGender} file={fileimg} 
              setfile={setFile} filename={filename} setfilename={setFilename} uploadedfile={uploadedfile} 
              setuploadedfile={setuploadedfile} downloadfile={downloadfile} setdownloadfile={setdownloadfile}/>
            } />
          <Route exact path="/signup" element={<Signup />} />
        </Routes>
    </Router>

  );

  
}

export default App;
