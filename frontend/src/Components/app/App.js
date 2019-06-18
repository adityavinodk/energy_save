import React from 'react';
import { BrowserRouter as Router, Switch, Route, Link } from 'react-router-dom';
import '../styles/app.css';
import Header from '../layout/Header';
import Footer from '../layout/Footer';
import Home from '../pages/Home';
import Dryer from '../pages/Dryer';

class App extends React.Component {
  render() {
    return (
      <Router>
        <div>
          <Header />
          <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
            <a className="navbar-brand" href="/">ENERGYSAVE</a>
            <ul className="navbar-nav mr-auto">
              <li><Link to={'/'} className="nav-item nav-link"> Home </Link></li>
            </ul>
          </nav>
          <main style={{
            paddingTop: "100px",
            paddingBottom: "50px",
            minHeight: "90vh",
            overflow: "hidden",
            display: "block",
            position: "relative",
          }}>
            <Switch>
              <Route exact path='/' component={Home} />
              <Route path='/dryer' component={Dryer} />
            </Switch>
          </main>
          <Footer />
        </div>
      </Router>
    );
  }
}
export default App;
