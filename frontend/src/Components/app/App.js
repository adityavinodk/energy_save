import React from 'react'
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom'
import '../styles/app.css'
// import Header from '../layout/Header';
import Footer from '../layout/Footer'
import Home from '../pages/Home'
import Dryer from '../pages/Appliances/Dryer'
import Monitor from '../pages/Appliances/Monitor'
import WashingMachine from '../pages/Appliances/WashingMachine'

class App extends React.Component {
  render () {
    return (
      <Router>
        <div>
          <nav className='navbar navbar-expand-md navbar-dark bg-dark'>
            <a
              className='navbar-brand text-success font-weight-bold mx-auto order-0'
              href='/'
            >
            <img src="/static/react/EnergySave.ico" width="20" height="20" class="d-inline-block" alt="" />
              {' '}EnergySave
            </a>
          </nav>
          <main
            style={{
              paddingTop: '100px',
              paddingBottom: '50px',
              minHeight: '90vh',
              overflow: 'hidden',
              display: 'block',
              position: 'relative'
            }}
          >
            <Switch>
              <Route exact path='/' component={Home} />
              <Route path='/dryer' component={Dryer} />
              <Route path='/monitor' component={Monitor} />
              <Route path='/washing_machine' component={WashingMachine} />
            </Switch>
          </main>
          <Footer />
        </div>
      </Router>
    )
  }
}
export default App
