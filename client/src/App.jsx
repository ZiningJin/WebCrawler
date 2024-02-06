import React from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css'
import Header from './components/Header/Header';
import Navigation from './components/Nav/Nav';
import Bci from './components/BCI/Bci';
import Pec from './components/PEC/Pec';
import Cceup from './components/CCEUP/Cceup';

const App = () => {
  return (
    <Router>
    <Navigation />
    <div style={{ paddingTop: '56px' }}> 
      <Route path="/Header" component={Header} />
    </div>
    <div style={{ paddingTop: '56px' }}> 
      <Route path="/Bci" component={Bci} />
    </div>
    <div style={{ paddingTop: '56px' }}> 
      <Route path="/Pec" component={Pec} />
    </div>
    <div style={{ paddingTop: '56px' }}> 
      <Route path="/Cceup" component={Cceup} />
    </div>
  </Router>

  )
}

export default App
