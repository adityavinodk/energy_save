import React from 'react';
import { BrowserRouter as Router, Switch, Route, Link } from 'react-router-dom';
import '../styles/app.css';
import Header from '../layout/Header';
import Footer from '../layout/Footer';
import Home from '../pages/home';
import Demo1 from '../pages/Demo1';
import Demo2 from '../pages/Demo2';

class App extends React.Component {
  render() {
    return (
      <Router>
        <div>
          <Header />
          <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
            <a class="navbar-brand" href="/">Navbar</a>
            <ul className="navbar-nav mr-auto">
              <li><Link to={'/'} className="nav-item nav-link"> Home </Link></li>
              <li><Link to={'/demo1'} className="nav-item nav-link">Demo1</Link></li>
              <li><Link to={'/demo2'} className="nav-item nav-link">Demo2</Link></li>
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
              <Route path='/demo1' component={Demo1} />
              <Route path='/demo2' component={Demo2} />
            </Switch>
          </main>
          <Footer />
        </div>
      </Router>
    );
  }
}
export default App;
