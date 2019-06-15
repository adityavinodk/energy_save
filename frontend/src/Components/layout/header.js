import React,{ Component } from 'react';
import { Link } from 'react-router-dom';
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
        <NavLink tag={Link} to="/" activeclassname="active">Page 1</NavLink>
      </NavItem>
      <NavItem>
        <NavLink tag={Link} to="/" activeclassname="active">Page 2</NavLink>
      </NavItem>
      <NavItem>
        <NavLink tag={Link} to="/" activeclassname="active">Page 3</NavLink>
      </NavItem>
    </Nav>
      </header>
    );
  }
}
export default Header;
