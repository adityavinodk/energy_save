import React,{ Component } from 'react';
import {
    Nav,
    NavItem,
    NavLink,
  } from 'reactstrap';
class Header extends Component {
  render(){
    return(
      <header>
      <Nav className="mr-auto" navbar>
      <NavItem>
        <NavLink to="/" activeclassname="active">Page 1</NavLink>
      </NavItem>
    </Nav>
      </header>
    );
  }
}
export default Header;
