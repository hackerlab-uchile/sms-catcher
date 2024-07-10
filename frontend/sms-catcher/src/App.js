// src/App.js
import React, { useState, useEffect } from 'react';
import Dashboard from './components/dashboard';
import fetchData from './services/apiService';
import './App.css';

const App = () => {
  const [modemInfo, setModemInfo] = useState({});

  useEffect(() => {
    const fetchModemInfo = async () => {
      try {
        const modemInfoData = await fetchData('http://127.0.0.1:8000/modem_info');
        setModemInfo(modemInfoData);
      } catch (error) {
        console.error('Error fetching modem info:', error);
      }
    };

    fetchModemInfo();
  }, []);

  // const handleUpdateModemInfo = async () => {
  //   try {
  //     await fetchData('http://127.0.0.1:8000/update_modem_info', 'POST');
  //     // After successfully sending the POST request, fetch the updated modem info
  //     const modemInfoData = await fetchData('http://127.0.0.1:8000/modem_info');
  //     setModemInfo(modemInfoData);
  //   } catch (error) {
  //     console.error('Error updating modem info:', error);
  //   }
  // };

  return (
    <div>
      <nav className="navbar">
        <h1 className="navbar-brand">SMS CATCHER</h1>
        {/* <button className="button" onClick={handleUpdateModemInfo}>Update Modem Info</button>*/}
      </nav>      
      <header className="App-header">
        <Dashboard />
      </header>
      <ul>
        {Object.entries(modemInfo).map(([modemIndex, modemData]) => (
          <li key={modemIndex} className="modem-index">
            <h3> MESSAGE_HASH {modemIndex}</h3>
            <ul>
              <p>Number: {modemData.number}</p>
              <p>Text: {modemData.text}</p>
              <p>URL: {modemData.url}</p>
            </ul>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default App;
