import React from 'react';
import './App.css';
import Header from '../layout/header';
import Footer from '../layout/footer';
import Home from '../pages/Home';
const App = () =>  {
  return (
    <div className="app-wrapper">
      <Header/>
      <main style={{
        paddingTop: "100px",
        paddingBottom: "50px",
        minHeight: "90vh",
        overflow: "hidden",
        display: "block",
        position: "relative",
      }}>
      <Home />
      </main>
      <Footer/>
    </div>
  );
}

export default App;
